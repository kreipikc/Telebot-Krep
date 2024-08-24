import sqlite3

# Обновление данных balance для пользователя
def updataBalance(balance: int, id: int) -> None:
    conn = sqlite3.connect('data/database/user_casino.sql')
    cur = conn.cursor()
    sql_update_query = f"""UPDATE user_casino SET balance = {balance} WHERE user_id = {id}"""
    cur.execute(sql_update_query)
    conn.commit()
    cur.close()
    conn.close()