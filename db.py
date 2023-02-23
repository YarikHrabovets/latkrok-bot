import pymysql.cursors
from constants import *


def open_connection():
    connection = pymysql.connect(
        user=USER,
        host=HOST,
        port=PORT,
        password=PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

    return connection


def get_user(user_id):
    connection = open_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM user WHERE user_id=%s', (user_id,))
            return cursor.fetchone()


def is_user_exist(user_id):
    connection = open_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM user WHERE user_id=%s', (user_id, ))
            return bool(cursor.fetchone())


def add_user(user_id, name):
    connection = open_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO user (user_id, name) VALUES (%s, %s)', (user_id, name))
            connection.commit()


def get_user_cart(user_id):
    connection = open_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM cart_product WHERE cart_id=%s', (user_id,))
            return cursor.fetchall()


def get_all_products():
    connection = open_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM product')
            return cursor.fetchall()


def get_product(id_):
    connection = open_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM product WHERE id=%s', (id_, ))
            return cursor.fetchone()


def get_price(id_):
    connection = open_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM price WHERE id=%s', (id_,))
            return cursor.fetchone()


def add_product(user_id, product_id, product_option, color, quantity):
    connection = open_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('''INSERT INTO cart_product (cart_id, product_id, product_option, color, quantity) 
            VALUES (%s, %s, %s, %s, %s)''', (user_id, product_id, product_option, color, quantity))
            connection.commit()


def delete_product(id_):
    connection = open_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM cart_product WHERE id=%s', (id_, ))
            connection.commit()


def delete_all_user_product(user_id):
    connection = open_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM cart_product WHERE cart_id=%s', (user_id, ))
            connection.commit()
