import sqlite3

contact = sqlite3.connect('dt.db')
cursor = contact.cursor()


def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY, 
    username TEXT NOT NULL,
    email TEXT NOT NULL, 
    age INT NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')


initiate_db()
'''for i in range(1, 5):
    cursor.execute('INSERT INTO Products(title, description, price) VALUES (?, ?, ?)',
                   (f'Продукт{i}', f"Описание{i}", f"{i * 100}"))
'''

s = []


def get_all_products():
    cursor.execute('SELECT * FROM Products')
    a = cursor.fetchall()
    s = []
    for i in a:
        s.append(list(i))
    contact.commit()
    return s



def is_include(username):
    a = cursor.execute(f'SELECT * FROM Users WHERE username=?', (username,))
    if a.fetchone() is None:
        contact.commit()
        b=False
    else:
        contact.commit()
        b=True
    return b



def add_user(username, email, age):
    cursor.execute(f'INSERT INTO Users VALUES(?, ?, ?, ?, ?)', (None, username, email, age, 1000))
    contact.commit()



