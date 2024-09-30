import sqlite3
from func_on_db import open_db, close_db

# Вывод всех пользователей
def printAllUsers():
    conn, cur = open_db()
    cur.execute("""SELECT * FROM user_casino""")
    user = cur.fetchall()
    for el in user:
        print(el[0], el[1], el[2], el[3])
    close_db(conn, cur)


# Закинуть деньги человеку
def addMoney(id: int, money: int) -> None:
    conn, cur = open_db()
    sql_update_query = f"""UPDATE user_casino SET balance = {money} WHERE user_id = {id}"""
    cur.execute(sql_update_query)
    close_db(conn, cur)


# Удалить пользователя
def deleteUser(id: int) -> None:
    conn, cur = open_db()
    cur.execute(f"""DELETE FROM user_casino WHERE user_id = {id}""")
    print(f"Пользователь с id: {id} удалён.")
    conn.commit()
    close_db(conn, cur)


# Вывод информации об определённом пользователе
def printUserInfo(id: int):
    conn, cur = open_db()
    cur.execute(f"""SELECT * FROM user_casino WHERE user_id = {id}""")
    user = cur.fetchall()
    print(user)
    for el in user:
        print(el[0], el[1], el[2], el[3])
    close_db(conn, cur)