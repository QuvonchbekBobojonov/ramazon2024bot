import sqlite3


def get_taqvim(region, date):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM taqvim WHERE region = '{region}' AND date = '{date}'")
    return cursor.fetchone()
