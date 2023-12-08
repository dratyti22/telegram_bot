import sqlite3 as sq
db = sq.connect('tg.db')
cur = db.cursor()


async def create_user_id_and_balance(user_id):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            {user_id} INTEGER PRIMARY KEY,
            balance INTEGER
        )
    '''.format(user_id=user_id))
    db.commit()
    db.close()
    print("подключена база данных")


async def add_balance(user_id, amount):
    # Получаем текущий баланс пользователя
    cur.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    current_balance = cur.fetchone()[0]

    # Прибавляем сумму к текущему балансу
    new_balance = current_balance + amount

    # Обновляем баланс в базе данных
    cur.execute("UPDATE users SET balance=? WHERE user_id=?", (new_balance, user_id))
    db.commit()
    db.close()
    print("база данных для пополнения подключенна")


async def subtract_balance(user_id, amount):
    # Получаем текущий баланс пользователя
    cur.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    current_balance = cur.fetchone()[0]
    print("База данных для вычета включенна")

    # Проверяем, достаточно ли средств на балансе для вычета
    if current_balance >= amount:
        new_balance = current_balance - amount
        # Обновляем баланс в базе данных
        cur.execute("UPDATE users SET balance=? WHERE user_id=?", (new_balance, user_id))
        db.commit()
        db.close()
        return True
    else:
        db.close()
        return False
