import sqlite3 as sq

with sq.connect("supplements.db") as connection:
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Products (
    title TEXT,
    description TEXT,
    price INTEGER
    )""")


def get_all_products():
    cursor.execute("SELECT title, description, price FROM Products")
    params = cursor.fetchall()
    return params
