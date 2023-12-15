import sqlite3 as sq

db = sq.connect('tg.db')
cur = db.cursor()


async def cmd_start_db(user_id):
    user = cur.execute("SELECT * FROM accounts WHERE tg_id == {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO accounts (tg_id) VALUES ({key})".format(key=user_id))
        db.commit()


class DataBaseUser:
    def __init__(self, db_file):
        self.db = sq.connect(db_file)
        self.cur = self.db.cursor()

    def user_exits(self, user_id):
        with self.db:
            results = cur.execute("SELECT * FROM accounts WHERE tg_id == {key}".format(key=user_id)).fetchone()
            return bool(len(results))

    def add_user(self, user_id):
        with self.db:
            return cur.execute("INSERT INTO accounts (tg_id) VALUES ({key})".format(key=user_id))

    def set_activate(self, user_id, activate):
        with self.db:
            return cur.execute("UPDATE accounts SET activate = ? WHERE tg_id == ?", (activate, user_id))

    def get_users(self):
        with self.db:
            return cur.execute("SELECT tg_id, activate FROM accounts").fetchall()
