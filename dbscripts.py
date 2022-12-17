import sqlite3 as sq

def create_db():
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS contracts (
        pid INTEGER NOT NULL,
        shop_name TEXT NOT NULL,
        wan_type TEXT NOT NULL,
        ip TEXT NOT NULL,
        legal_entity TEXT NOT NULL,
        isp TEXT NOT NULL,
        contract TEXT NOT NULL,
        shop_address TEXT NOT NULL,
        sd_phone TEXT,
        sd_email TEXT
    )
    """
    cursor.execute(query)
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
    query = f"""SELECT * FROM contracts
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

create_db()