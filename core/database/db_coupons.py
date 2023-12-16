import sqlite3 as sq

conn = sq.connect('tg.db')
cursor = conn.cursor()


async def create_coupons():
    cursor.execute('''CREATE TABLE IF NOT EXISTS coupons (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price INTEGER,
        quantity INTEGER
    )''')
    conn.commit()


async def add_coupons(name: str, price: int, quantity: int):
    cursor.execute("INSERT INTO coupons (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity,))
    conn.commit()


async def deleted_coupons(id_coupons):
    cursor.execute("DELETE FROM coupons WHERE id=?", (id_coupons,))
    cursor.execute("UPDATE coupons SET id = id - 1 WHERE id > ?", (id_coupons,))
    conn.commit()


async def display_coupons():
    cursor.execute("SELECT * FROM coupons")
    entry = cursor.fetchall()
    conn.commit()
    return entry


async def get_coupon_details(coupon_name: str):
    cursor.execute("SELECT price, quantity FROM coupons WHERE name = ?", (coupon_name,))
    result = cursor.fetchone()
    if result:
        return result
    return None, None


async def decrement_coupon_amount(coupon_name: str):
    cursor.execute("UPDATE coupons SET quantity = quantity - 1 WHERE name = ?", (coupon_name,))
    conn.commit()