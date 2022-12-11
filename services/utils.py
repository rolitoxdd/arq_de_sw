import sqlite3
import os


def str_bus_format(data, service_name='g7999'):
    total_digits = 5

    transformed_data = str(data)

    transformed_data_len = len(transformed_data)

    digits_left = total_digits - len(str(transformed_data_len))

    str_data_lenght = ''

    for i in range(digits_left):
        str_data_lenght += '0'

    str_data_lenght += str(transformed_data_len) + \
        service_name+transformed_data

    return str_data_lenght


def create_tables():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''CREATE TABLE IF NOT EXISTS users
            (
                rut text PRIMARY KEY,
                email text, 
                name text, 
                password text,
                type integer DEFAULT 0 
            )
            '''
    )

    c.execute(
        '''CREATE TABLE IF NOT EXISTS maquinarias
            (
                id integer PRIMARY KEY AUTOINCREMENT,
                nombre text,
                estado text,
                costo integer,
                fecha_ingreso datetime DEFAULT CURRENT_DATE,
                fecha_salida datetime
            )
        '''
    )

    c.execute(
        '''CREATE TABLE IF NOT EXISTS componentes
            (
                id integer PRIMARY KEY AUTOINCREMENT,
                id_maquinaria integer,
                nombre text,
                estado text,
                marca text,
                modelo text,
                costo integer,
                fecha_ingreso datetime DEFAULT CURRENT_DATE,
                fecha_salida datetime,
                FOREIGN KEY (id_maquinaria) REFERENCES maquinarias (id)
            )
        '''
    )

    conn.commit()
    conn.close()


def remove_db():
    try:
        os.remove('db.sqlite3')
    except:
        pass


def insert_user(email, name, password, rut, type):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''INSERT INTO users (email, name, password, rut, type) VALUES (?, ?, ?, ?, ?)''',
        (email, name, password, rut, type)
    )

    conn.commit()
    conn.close()


def insert_maquinaria(nombre, estado, costo):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''INSERT INTO maquinarias (nombre, estado, costo) VALUES (?, ?, ?)''',
        (nombre, estado, costo)
    )

    conn.commit()
    conn.close()


def consulta_maquinaria(id_maquinaria=''):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    if id_maquinaria == '':
        c.execute('''SELECT * FROM maquinarias''')
    else:
        c.execute(
            '''SELECT * FROM maquinarias WHERE id = ?''', (id_maquinaria,))
    res = c.fetchall()
    conn.commit()
    conn.close()
    return res


def update_maquinaria(id_maquinaria, nombre, estado, costo):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''UPDATE maquinarias SET nombre = ?, estado = ?, costo = ? WHERE id = ?''',
        (nombre, estado, costo, id_maquinaria)
    )

    conn.commit()
    conn.close()
    return c.rowcount


def delete_maquinaria(id_maquinaria):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''UPDATE maquinarias SET fecha_salida = CURRENT_DATE WHERE id = ?''',
        (id_maquinaria)
    )

    conn.commit()
    conn.close()
    return c.rowcount


def insert_componente(id_maquinaria, nombre, estado, marca, modelo, costo):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''INSERT INTO componentes (id_maquinaria, nombre, estado, marca, modelo, costo) VALUES (?, ?, ?, ?, ?, ?)''',
        (id_maquinaria, nombre, estado, marca, modelo, costo)
    )

    conn.commit()
    conn.close()
    return c.rowcount


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def w_print(*text):
    print(bcolors.WARNING, *text, bcolors.ENDC)


def g_print(*text):
    print(bcolors.OKGREEN, *text, bcolors.ENDC)


def f_print(*text):
    print(bcolors.FAIL, *text, bcolors.ENDC)


def b_print(*text):
    print(bcolors.OKBLUE, *text, bcolors.ENDC)


def h_print(*text):
    print(bcolors.HEADER, *text, bcolors.ENDC)


def u_print(*text):
    print(bcolors.UNDERLINE, *text, bcolors.ENDC)


if __name__ == '__main__':
    remove_db()
    create_tables()
    insert_user('admin@email.com', 'admin', 'admin',
                '12345678-9', 0)  # admin (type 0)
