# AGENTS.md — ISPinfo

Внутренний веб-сервис для сотрудников: хранит базу договоров с интернет-провайдерами по магазинам и автоматически формирует тексты заявок в техподдержку провайдеров при проблемах с каналом.

## Стек

- **Backend:** Python, Flask (единый файл `app.py`)
- **Auth:** Flask-Login (кастомный `UserLogin`), локальные пароли (werkzeug `pbkdf2:sha256`) + LDAP (`ldap3`)
- **DB:** SQLite, путь задаётся переменной `DB_PATH` (по умолчанию `src/database.db`; в Docker — `/app/data/database.db`, см. compose)
- **Импорт данных:** openpyxl (Excel `.xlsx`)
- **Конфиг:** `python-dotenv`, файл `.env` в корне (в `.gitignore`)
- **Frontend:** Jinja2-шаблоны + один CSS (`static/css/styles.css`), без JS-фреймворков
- **requirements.txt:** `flask`, `flask-login`, `openpyxl`, `ldap3`, `python-dotenv`, `gunicorn` (werkzeug подтягивается с flask)

## Структура проекта

```
ISPinfo/
├── src/                        # все исходники
│   ├── app.py                  # Flask-приложение (роуты, сессия, login_manager)
│   ├── dbscripts.py            # SQLite, импорт Excel, LDAP, UserLogin
│   ├── init_db.py              # первичная инициализация БД и admin
│   ├── applicationTemplate.txt # шаблон текста заявки (справочно)
│   ├── testContracts.xlsx      # пример файла для импорта
│   ├── templates/              # Jinja2-шаблоны
│   └── static/                 # css/, images/
├── docker/
│   ├── Dockerfile              # python:3.12-slim + gunicorn
│   └── docker-compose.yml      # проект `ispinfo`, порт 8080, volume ./data
├── .dockerignore               # в корне: контекст сборки = корень проекта
├── .env.example                # шаблон LDAP-переменных
├── requirements.txt
└── data/                       # runtime: database.db (в .gitignore)
```

Flask ищет `templates/` и `static/` относительно каталога `app.py`, поэтому запуск — `python src/app.py` (из любого каталога).

## Запуск

```bash
python src/app.py   # host 0.0.0.0, debug=True
```

Важно: `src/dbscripts.py` на импорте читает обязательные переменные `LDAP_SERVER`, `LDAP_USER`, `LDAP_USER_CN`, `SEARCH_USER_CATALOG` из `.env` в корне проекта (ищет и там, и в `src/`) — без них приложение падает при старте (KeyError), даже если LDAP не используется.

Первичная инициализация БД:
- **Docker:** автоматически через `src/init_db.py` при первом старте контейнера
- **Локально:** `python src/init_db.py` (создаёт таблицы и пользователя `admin`, пароль: `1488`); либо вручную `create_db()` + `create_admin()` в `dbscripts.py`

### Запуск в Docker (рекомендуемый способ)

```bash
cp .env.example .env   # заполнить LDAP-переменные
docker compose -f docker/docker-compose.yml up -d --build
# приложение: http://<IP-машины>:8080
```

- `docker/Dockerfile` — python:3.12-slim, gunicorn (2 воркера), **без debug-режима**; контекст сборки — корень проекта, копируется только `src/` + `requirements.txt`
- `docker/docker-compose.yml` — явный `name: ispinfo` (иначе compose назовёт проект `docker` по имени каталога), проброс `8080:5000`, volume `../data:/app/data`, `env_file: ../.env`
- `src/init_db.py` — при первом старте (если БД отсутствует) создаёт таблицы и пользователя admin
- Путь к БД задаётся переменной `DB_PATH` (в `dbscripts.py`); в compose выставлен `/app/data/database.db`, локально по умолчанию `src/database.db`
- БД хранится в `./data/database.db` на хосте — переживает пересборку контейнера
- `.env` в контейнер не монтируется: переменные попадают через `env_file` в окружение, `load_dotenv` в `dbscripts.py` просто не срабатывает (файл отсутствует, guard `os.path.exists`)

## Архитектура

Простая трёхслойная структура без ORM:

```
src/app.py       — все Flask-роуты, сессия, login_manager (только glue-код)
src/dbscripts.py — вся работа с SQLite (f-строки SQL, без параметризации),
                   импорт Excel, LDAP-аутентификация, класс UserLogin
src/templates/   — Jinja2: base.html (nav), index, searchResult, application,
                   update, usermgmt, login, about
src/static/      — css/styles.css, images/
```

- `app.py` не содержит бизнес-логики — только валидация входа и передача данных в шаблоны.
- `dbscripts.py` — единственный модуль с логикой; каждый запрос открывает/закрывает своё соединение.
- Шаблоны получают `class1..class4` (активный пункт меню) и `user`/`usertype` из сессии.

## База данных (SQLite, `database.db`)

### Таблица `contracts` (договоры с провайдерами)
| # | колонка | описание |
|---|---------|----------|
| 0 | id | PK, AUTOINCREMENT |
| 1 | pid | PID магазина |
| 2 | shop_name | название магазина |
| 3 | wan_type | тип канала |
| 4 | ip | IP-адрес |
| 5 | legal_entity | юридическое лицо |
| 6 | isp | провайдер |
| 7 | contract | номер договора |
| 8 | shop_address | адрес магазина |
| 9 | sd_phone | телефон техподдержки |
| 10 | sd_email | почта техподдержки |

### Таблица `users`
| # | колонка | описание |
|---|---------|----------|
| 0 | id | PK |
| 1 | username | логин (UNIQUE) |
| 2 | psw | хеш пароля (werkzeug) или `'-'` для LDAP-пользователей |
| 3 | user_type | `Admin` или `Support` |
| 4 | auth_type | `Local` или `LDAP` |

Роли: `Admin` видит в меню «Актуализация» (импорт) и «Пользователи»; `Support` — только поиск и заявки.

## Формат импортируемого Excel

Файл `.xlsx`, активный лист, **1-я строка — заголовок**, данные с 2-й строки. Колонки строго по порядку:
`A=pid, B=shop_name, C=wan_type, D=ip, E=legal_entity, F=isp, G=contract, H=shop_address, I=sd_phone, J=sd_email`

Пример: `testContracts.xlsx`.
⚠️ Импорт **полностью заменяет** таблицу: сначала `DELETE FROM contracts`, затем вставка всех строк (см. `db_update`).

## Роуты

| Метод | URL | Назначение |
|-------|-----|------------|
| GET | `/` | главная (поиск) или редирект на login |
| POST | `/search` | поиск по `pid` (точное) или `shop` (LIKE %...%); скрытое поле `searchType` |
| POST | `/application/<id>` | показать сформированную заявку по договору |
| GET/POST | `/update` | импорт xlsx (только авторизованные) |
| GET | `/about` | о приложении |
| GET | `/usermgmt` | список пользователей |
| POST | `/adduser` | добавить пользователя (username, usertype, auth) |
| POST | `/deleteuser/<id>` | удалить пользователя |
| GET/POST | `/login` | вход (Local: хеш; LDAP: bind через ldap3) |
| GET | `/logout` | выход |

Текст заявки формируется в `templates/application.html` по шаблону из `applicationTemplate.txt` (обращение от юр.лица, договор, адрес, IP, просьба проверить услугу + почта техподдержки).

## Ключевые функции `dbscripts.py`

- `create_db()` / `create_admin()` — инициализация (в Docker вызывается автоматически из `src/init_db.py`, локально — `python src/init_db.py`)
- `get_contracts_pid(pid)` / `get_contracts_shop(shop)` / `get_contract_id(id)` — поиск
- `db_update(file)` — импорт Excel (полная замена данных)
- `login(login, password)` — вход: `Local` → `check_password_hash`, `LDAP` → `ldap_auth()`
- `ldap_auth(login, password)` — поиск по `sAMAccountName` в `SEARCH_USER_CATALOG`, затем bind
- `getAllUsers()` / `getUser(id)` / `adduser(...)` / `deleteUser(id)` — управление пользователями
- `UserLogin` — адаптер для Flask-Login (`is_authenticated`, `is_active`, `is_anonymous`, `get_id`)

## Известные проблемы / на что обратить внимание при правках

1. **SQL-инъекции:** все запросы собраны f-строками (и в `dbscripts.py`, и в `login`). При рефакторинге переводить на параметризованные запросы.
2. **`SECRET_KEY` захардкожен** в `app.py` (`'aboba1488'`) — сессии небезопасны; вынести в `.env`.
3. **`debug=True`** при запуске в `__main__`.
4. **`/search` не проверяет авторизацию** (в отличие от остальных роутов) — любой неавторизованный запрос упадёт на `session['username']`.
5. `db_update` глотает все исключения (`except:`) и возвращает False; в except-ветке `conn.close()` может быть не определён, если упало `load_workbook`.
6. В `usermgmt.html` защита от удаления себя/admin сделана только на UI (disabled) — на бэкенде `/deleteuser` не проверяет роль.
7. `get_data()` обращается к несуществующей таблице `shops` (мёртвый код).
8. `delete_all_data()` — мёртвый код.
9. `create_admin()` делает INSERT без проверки существования — повторный вызов упадёт (UNIQUE username).
10. Импортируемые значения не валидируются и не экранируются (см. п.1) — кавычки в данных Excel сломают INSERT.

## Файлы

- `src/app.py` — приложение
- `src/dbscripts.py` — DB/импорт/LDAP
- `src/init_db.py` — инициализация БД
- `src/templates/`, `src/static/` — фронтенд
- `src/applicationTemplate.txt` — шаблон текста заявки (справочно)
- `src/testContracts.xlsx` — пример файла для импорта
- `docker/Dockerfile`, `docker/docker-compose.yml`, `.dockerignore` — docker-развертка
- `requirements.txt` — зависимости (flask, flask-login, openpyxl, ldap3, python-dotenv, gunicorn)
- `.env` (не в git) — LDAP_SERVER, LDAP_USER, LDAP_USER_CN, SEARCH_USER_CATALOG
