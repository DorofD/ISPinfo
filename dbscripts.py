import sqlite3 as sq
import openpyxl
from ldap3 import Connection
from werkzeug.security import generate_password_hash, check_password_hash
import os

def create_db():
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    query = """CREATE TABLE IF NOT EXISTS contracts (
        id INTEGER NOT NULL UNIQUE, 
        pid INTEGER NOT NULL,
        shop_name TEXT NOT NULL,
        wan_type TEXT NOT NULL,
        ip TEXT,
        legal_entity TEXT NOT NULL,
        isp TEXT NOT NULL,
        contract TEXT,
        shop_address TEXT NOT NULL,
        sd_phone TEXT,
        sd_email TEXT,
        PRIMARY KEY ("id" AUTOINCREMENT)
    )
    """
    cursor.execute(query)
    
    query = """CREATE TABLE IF NOT EXISTS users (
        id INTEGER UNIQUE, 
        username TEXT NOT NULL UNIQUE,
        psw TEXT NOT NULL,
        user_type TEXT NOT NULL,
        auth_type TEXT NOT NULL,
        PRIMARY KEY ("id" AUTOINCREMENT)
    )
    """
    cursor.execute(query)
    conn.close()

def create_admin():
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    query = """INSERT INTO users (username, psw, user_type, auth_type) 
                VALUES ('admin', 'pbkdf2:sha256:260000$QXnsaEQce8nu6M5s$878f380fa0e24f15ee8142a1b4cb054c048feda759445678c306f9ddeaae5bce', 'Admin', 'Local')"""
    cursor.execute(query)
    conn.commit()
    conn.close()

def get_data():
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM shops""")
    for result in cursor:
        print(result)
    conn.close()
    
def get_contracts_pid(pid):
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    query = f"""SELECT * FROM contracts
        WHERE pid = '{pid}'"""
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def get_contracts_shop(shop_name):
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    query = f"""SELECT * FROM contracts
        WHERE shop_name LIKE '%{shop_name}%'"""
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result
    
def get_contract_id(id):
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    query = f"""SELECT * FROM contracts
        WHERE id = '{id}'"""
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

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
def ldap_auth(login, password):
    try:
        conn = Connection(os.environ['ldap_server'], os.environ['ldap_user_cn'], os.environ['ldap_user'], auto_bind=True)
        conn.search(os.environ['search_user_catalog'], f'(sAMAccountName={login})', attributes=['Name'])
        name = conn.entries[0]['Name']
        conn = Connection(os.environ['ldap_server'], f"CN={name},{os.environ['search_user_catalog']}", password, auto_bind=True, raise_exceptions=True)
        return True
    except:
        return False

def login(login, password):
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    query = f"""SELECT * FROM users
        WHERE username = '{login}'"""
    cursor.execute(query)
    user = cursor.fetchall()
    conn.close()
    print(user)
    if user:
        if user[0][4] == 'Local':
            if check_password_hash(user[0][2], password):
                print('local success')
                return user[0]
            else:
                print('local fail')
                return False
        elif user[0][4] == 'LDAP':
            if ldap_auth(login, password):
                print('ldap success')
                return user[0]
            else:
                print('ldap fail')
                return False
    else:
        print('user not found')
        return False

def getAllUsers():
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    query = f"""SELECT * FROM users"""
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def getUser(user_id):
    conn = sq.connect('database.db')
    cursor = conn.cursor()
    query = f"""SELECT * FROM users
        WHERE id = '{user_id}'"""
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result[0]

def deleteUser(user_id):
    try:
        conn = sq.connect('database.db')
        cursor = conn.cursor()
        query = f"""
            DELETE FROM users
            WHERE id = '{user_id}'"""
        cursor.execute(query)
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def adduser(username, usertype, auth):
    try:
        conn = sq.connect('database.db')
        cursor = conn.cursor()
        query = f"""INSERT INTO users (username, psw, user_type, auth_type) 
                    VALUES ('{username}', '-', '{usertype}', '{auth}')"""
        cursor.execute(query)
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


class UserLogin():
    def fromDB(self, user_id):
        self.__user = getUser(user_id)
        return self
    
    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user[0])

# hash = generate_password_hash('1488')
# print(hash)
# print(check_password_hash(hash, '1488'))

# create_db()
# create_admin()
