import sqlite3
from typing import List, Tuple, Optional


class DatabaseUser:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('data\\database\\user_casino.sql')
        self.cur = self.conn.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS user_casino (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id int, balance int, username varchar(50))""")
        self.conn.commit()
        self.close_db()

    def open_db(self) -> None:
        self.conn = sqlite3.connect('data\\database\\user_casino.sql')
        self.cur = self.conn.cursor()

    def close_db(self) -> None:
        self.cur.close()
        self.conn.close()


class DatabaseUserCrud(DatabaseUser):
    def add_user_db(self, user_id: int, user_name: str) -> None:
        self.open_db()
        self.cur.execute(f"""SELECT * FROM user_casino WHERE user_id = {user_id}""")
        user = self.cur.fetchall()

        # Если пользователь с таким user_id отсутствует -> создаем нового пользователя в БД
        if not user:
            self.cur.execute("""INSERT INTO user_casino (id, user_id, balance, username) VALUES (NULL, '%s', %s, '%s')""" % (
            user_id, 1000, user_name))
            self.conn.commit()

        self.close_db()

    def get_user_db(self, user_id: int) -> Optional[List[Tuple[int]]]:
        self.open_db()
        self.cur.execute(f"""SELECT * FROM user_casino WHERE user_id = {user_id}""")
        user = self.cur.fetchall()
        self.close_db()
        return user

    def print_all_users(self) -> None:
        self.open_db()
        self.cur.execute("""SELECT * FROM user_casino""")
        user = self.cur.fetchall()
        for el in user:
            print(el[0], el[1], el[2], el[3])
        self.close_db()

    def print_user_info(self, user_id: int) -> None:
        self.open_db()
        self.cur.execute(f"""SELECT * FROM user_casino WHERE user_id = {user_id}""")
        user = self.cur.fetchall()
        print(user)
        for el in user:
            print(el[0], el[1], el[2], el[3])
        self.close_db()

    def delete_user(self, user_id: int) -> None:
        self.open_db()
        self.cur.execute(f"""DELETE FROM user_casino WHERE user_id = {user_id}""")
        print(f"Пользователь с id: {user_id} удалён.")
        self.conn.commit()
        self.close_db()

    def update_balance(self, balance: int, user_id: int) -> None:
        self.open_db()
        sql_update_query = f"""UPDATE user_casino SET balance = {balance} WHERE user_id = {user_id}"""
        self.cur.execute(sql_update_query)
        self.conn.commit()
        print("UPDATE", balance)
        self.close_db()

    def add_money(self, user_id: int, money: int) -> None:
        self.open_db()
        sql_update_query = f"""UPDATE user_casino SET balance = {money} WHERE user_id = {user_id}"""
        self.cur.execute(sql_update_query)
        self.close_db()