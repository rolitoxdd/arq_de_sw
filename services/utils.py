import sqlite3


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

    x = c.execute(
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

    conn.commit()
    conn.close()


def drop_tables():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    x = c.execute(
        '''DROP TABLE IF EXISTS users'''
    )

    conn.commit()
    conn.close()


def insert_user(email, name, password, rut, type):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    x = c.execute(
        '''INSERT INTO users (email, name, password, rut, type) VALUES (?, ?, ?, ?, ?)''',
        (email, name, password, rut, type)
    )

    conn.commit()
    conn.close()


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


if __name__ == '__main__':
    drop_tables()
    create_tables()
    insert_user('admin@email.com', 'admin', 'admin',
                '12345678-9', 0)  # admin (type 0)
