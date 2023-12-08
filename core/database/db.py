# пока используется sqllite3, но потом перенесу на psypg2
import sqlite3 as sq

conn = sq.connect('text_prices.db')
cursor = conn.cursor()


async def create_database_prices_text():
    # Создаем таблицу для текста и цены
    cursor.execute('''CREATE TABLE IF NOT EXISTS text_prices
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       text TEXT NOT NULL,
                       price REAL NOT NULL)''')

    conn.commit()
    print("База данных создана")


# Функция для добавления новой записи в базу данных
async def add_entry(text, price):
    # Получаем максимальное значение идентификатора и увеличиваем его на 1 для новой записи
    cursor.execute("SELECT MAX(id) FROM text_prices")
    max_id = cursor.fetchone()[0]
    new_id = max_id + 1 if max_id else 1

    cursor.execute("INSERT INTO text_prices (id, text, price) VALUES (?, ?, ?)", (new_id, text, price))
    print("Товар добавлен в базу данных")
    conn.commit()


# Функция для удаления записи из базы данных
async def delete_entry(entry_id):

    cursor.execute("DELETE FROM text_prices WHERE id=?", (entry_id,))

    # Уменьшаем значения идентификаторов всех последующих записей
    cursor.execute("UPDATE text_prices SET id = id - 1 WHERE id > ?", (entry_id,))

    # Сохраняем изменения в базе данных
    conn.commit()


async def display_entries_admin():
    entries = []
    cursor.execute("SELECT id, text, price FROM text_prices")

    for entry in cursor.fetchall():
        entries.append(entry)

    conn.commit()
    return entries


async def display_entries_user():
    entries = []
    cursor.execute("SELECT text, price FROM text_prices")

    for entry in cursor.fetchall():
        entries.append(entry)

    conn.commit()
    return entries
