import sqlite3 as sq

def create_db():
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS shops (
    pid	INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
        )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS contracts (
    ptid INTEGER NOT NULL,
    type TEXT NOT NULL,
    number TEXT NOT NULL,
    sdemail TEXT
        )""")
    conn.close()

def get_data():
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM shops""")
    for result in cursor:
        print(result)
    conn.close()
    
def get_contracts(pid):
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    query = f"""SELECT shops.pid, shops.name, contracts.type, contracts.number, contracts.sdemail FROM shops, contracts
        ON contracts.ptid = shops.pid
        WHERE pid = '{pid}'"""
    # try:
    cursor.execute(query)
    result= cursor.fetchall()
    # result = f'{shop[0][0]} {shop[0][1]}'
    conn.close()
    return result
    # except:
    #     conn.close()
    #     return 'PID не найден'

def set_data():
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    # pid = int(input('PID: '))
    # shop = str(input('Shop name: '))
    pid = 156
    shop = 'Магазин (город)'
    cursor.execute(f"""INSERT INTO shops (pid, name) VALUES ('{pid}', '{shop}')""")
    conn.commit()
    conn.close()
