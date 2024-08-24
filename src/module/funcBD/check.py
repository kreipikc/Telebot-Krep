import sqlite3

def openBD():
    conn = sqlite3.connect('data/database/user_casino.sql')
    cur = conn.cursor()
    return conn, cur

# Вывод всех пользователей
def printAllUsers():
    conn, cur = openBD()
    cur.execute("""SELECT * FROM user_casino""")
    user = cur.fetchall()
    for el in user:
        print(el[0], el[1], el[2], el[3])
    cur.close()
    conn.close()

# Закинуть деньги человеку
def addMoney(id: int, money: int) -> None:
    conn, cur = openBD()
    sql_update_query = f"""UPDATE user_casino SET balance = {money} WHERE user_id = {id}"""
    cur.execute(sql_update_query)
    cur.close()
    conn.close()

# Удалить пользователя
def deleteUser(id: int) -> None:
    conn, cur = openBD()
    cur.execute(f"""DELETE FROM user_casino WHERE user_id = {id}""")
    print(f"Пользователь с id: {id} удалён.")
    conn.commit()
    cur.close()
    conn.close()

# Вывод информации об определённом пользователе
def printUserInfo(id: int):
    conn, cur = openBD()
    cur.execute(f"""SELECT * FROM user_casino WHERE user_id = {id}""")
    user = cur.fetchall()
    print(user)
    for el in user:
        print(el[0], el[1], el[2], el[3])
    cur.close()
    conn.close()