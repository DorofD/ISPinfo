import sqlite3 as sq
import openpyxl
import ldap3

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


from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError


def global_ldap_authentication(user_name, user_pwd):
    """
      Function: global_ldap_authentication
       Purpose: Make a connection to encrypted LDAP server.
       :params: ** Mandatory Positional Parameters
                1. user_name - LDAP user Name
                2. user_pwd - LDAP User Password
       :return: None
    """

    # fetch the username and password
    ldap_user_name = user_name.strip()
    ldap_user_pwd = user_pwd.strip()

    # ldap server hostname and port
    ldsp_server = f"ldap://192.168.8.237:389"

    # dn
    root_dn = "dc=bookcentre,dc=ru"

    # user
    user = f"cn={ldap_user_name},{root_dn},ou='ProgrammService'"

    print(user)
    server = Server(ldsp_server, get_info=ALL)

    connection = Connection(server,
                            user=user,
                            password=ldap_user_pwd)
    if not connection.bind():
        print(f" *** Cannot bind to ldap server: {connection.last_error} ")
        l_success_msg = f' ** Failed Authentication: {connection.last_error}'
    else:
        print(f" *** Successful bind to ldap server")
        l_success_msg = 'Success'

    return l_success_msg

# global_ldap_authentication('servicedesk', 'servicedesk')