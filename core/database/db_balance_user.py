import sqlite3 as sq

conn = sq.connect('tg.db')
cursor = conn.cursor()


async def create_user_id_and_balance(user_id):
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS users (
             user_id INTEGER PRIMARY KEY,
             balance INTEGER
         )
     ''')
    conn.commit()

    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    existing_user = cursor.fetchone()

    if existing_user is None:
        cursor.execute('INSERT INTO users (user_id, balance) VALUES (?, ?)', (user_id, 0,))
        conn.commit()


async def add_balance(user_id, amount):
    cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    cursor_balance = cursor.fetchone()[0]
    new_balance = cursor_balance + amount
    cursor.execute("UPDATE users SET balance=? WHERE user_id=?", (new_balance, user_id))
    conn.commit()
    print("База данных для пополнения подключена")


async def subtract_balance(user_id, amount):
    # Получаем текущий баланс пользователя
    cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    cursor_balance = cursor.fetchone()[0]
    print("База данных для вычета включена")

    # Проверяем, достаточно ли средств на балансе для вычета
    if cursor_balance >= amount:
        new_balance = cursor_balance - amount
        # Обновляем баланс в базе данных
        cursor.execute("UPDATE users SET balance=? WHERE user_id=?", (new_balance, user_id))
        conn.commit()


async def display_balance(user_id: int):
    cursor.execute("SELECT balance, user_id FROM users WHERE user_id = ?", (user_id,))
    entry = cursor.fetchone()
    conn.commit()
    return entry
