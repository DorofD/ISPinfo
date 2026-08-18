# Контекст сборки — корень проекта (см. docker/docker-compose.yml)
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

# БД и переменные окружения — извне (см. docker/docker-compose.yml)
VOLUME ["/app/data"]

EXPOSE 5000

# Инициализация БД при первом старте + gunicorn (без debug-режима)
CMD ["sh", "-c", "python init_db.py && gunicorn -b 0.0.0.0:5000 --workers 2 app:app"]
