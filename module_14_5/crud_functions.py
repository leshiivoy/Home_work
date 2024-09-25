import sqlite3


def initiate_db():
    connection = sqlite3.connect("supplements.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL DEFAULT 1000
        )
    ''')

    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect("supplements.db")
    cursor = connection.cursor()
    cursor.execute("SELECT title, description, price FROM Products")
    params = cursor.fetchall()
    return params


def add_user(username, email, age):
    connection = sqlite3.connect("supplements.db")
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)', (username, email, age))
    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect("supplements.db")
    cursor = connection.cursor()
    cursor.execute('SELECT EXISTS(SELECT 1 FROM Users WHERE username = ?)', (username,))
    exists = cursor.fetchone()[0]
    connection.close()
    return exists


