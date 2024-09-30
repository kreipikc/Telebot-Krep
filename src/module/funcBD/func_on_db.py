import sqlite3
from typing import List, Tuple
from sqlite3 import Connection, Cursor

# Откртие БД
def open_db() -> {Connection, Cursor}:
    conn = sqlite3.connect('data/database/user_casino.sql')
    cur = conn.cursor()
    return conn, cur


# Закрытие БД
def close_db(conn: Connection, cur: Cursor) -> None:
    cur.close()
    conn.close()


# Обновление данных balance для пользователя
def updataBalance(balance: int, id: int) -> None:
    conn, cur = open_db()
    sql_update_query = f"""UPDATE user_casino SET balance = {balance} WHERE user_id = {id}"""
    cur.execute(sql_update_query)
    conn.commit()
    print("UPDATE", balance)
    close_db(conn, cur)


# Создание БД, если её нет
def createdDB() -> None:
    conn, cur = open_db()
    cur.execute("""CREATE TABLE IF NOT EXISTS user_casino (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id int, balance int, username varchar(50))""")
    conn.commit()
    close_db(conn, cur)


# Добавление пользователя в БД, если его нет
def add_user_db(user_id: int, user_name: str) -> None:
    conn, cur = open_db()
    cur.execute(f"""SELECT * FROM user_casino WHERE user_id = {user_id}""")
    user = cur.fetchall()
    
    # Если пользователь с таким user_id отсуствует -> создаем нового пользователя в БД
    if user == []:
        cur.execute("""INSERT INTO user_casino (id, user_id, balance, username) VALUES (NULL, '%s', %s, '%s')""" % (user_id, 1000, user_name))
        conn.commit()
        
    close_db(conn, cur)


# Получение информации о пользователе
def get_user_db(user_id: int) -> List[Tuple[int]]:
    conn, cur = open_db()
    cur.execute(f"""SELECT * FROM user_casino WHERE user_id = {user_id}""")
    user = cur.fetchall()
    close_db(conn, cur)
    return user