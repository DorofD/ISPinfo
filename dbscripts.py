import sqlite3 as sq

def create_db():
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS shops (
    pid	INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
        )""")
    # cur.execute("""CREATE TABLE IF NOT EXISTS contracts (
    # pid	INTEGER PRIMARY KEY,
    # name TEXT NOT NULL UNIQUE
    #     )""")
    conn.close()

def get_data():
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM shops""")
    for result in cursor:
        print(result)
    conn.close()
    
def get_shop(pid):
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f"""SELECT * FROM shops
        WHERE pid = '{pid}'""")
        shop = cursor.fetchall()
        result = f'{shop[0][0]} {shop[0][1]}'
        conn.close()
        return result
    except:
        conn.close()
        return 'PID не найден'

def set_data():
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    # pid = int(input('PID: '))
    # shop = str(input('Shop name: '))
    pid = 156
    shop = 'Залупа (город)'
    cursor.execute(f"""INSERT INTO shops (pid, name) VALUES ('{pid}', '{shop}')""")
    conn.commit()
    conn.close()

print(get_shop(123))
