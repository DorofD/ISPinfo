import sqlite3 as sq
import openpyxl

def create_db():
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS contracts (
        pid INTEGER NOT NULL,
        shop_name TEXT NOT NULL,
        wan_type TEXT NOT NULL,
        ip TEXT,
        legal_entity TEXT NOT NULL,
        isp TEXT NOT NULL,
        contract TEXT,
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

def delete_all_data():
        conn = sq.connect('database.db')
        cursor = conn.cursor()
        query = """
            SELECT * FROM contracts
        """
        cursor.execute(query)
        query = """
            DELETE FROM contracts
        """
        cursor.execute(query)
        conn.commit()
        conn.close()

def db_update(file):
    try:
        conn = sq.connect('database.db')
        cursor = conn.cursor()
        wb = openpyxl.load_workbook(file) # подключение листа Excel
        sheet = wb.active
        # перед действием ниже нужно дописать проверки импортированного файла
        query = """
            SELECT * FROM contracts
        """
        cursor.execute(query)
        query = """
            DELETE FROM contracts
        """
        cursor.execute(query)
        # range(len(sheet["A"]) - 1)
        i = 1
        for row in range(len(sheet["A"]) - 2):
            if sheet['A'][i].value:
                query = f""" 
                    INSERT INTO contracts (pid, shop_name, wan_type, ip, legal_entity, isp, contract, shop_address, sd_phone, sd_email) 
                    VALUES ('{sheet['A'][i].value}',
                    '{sheet['B'][i].value}',
                    '{sheet['C'][i].value}',
                    '{sheet['D'][i].value}',
                    '{sheet['E'][i].value}',
                    '{sheet['F'][i].value}',
                    '{sheet['G'][i].value}',
                    '{sheet['H'][i].value}',
                    '{sheet['I'][i].value}',
                    '{sheet['J'][i].value}'
                    )
                """
                cursor.execute(query)
                i += 1
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

