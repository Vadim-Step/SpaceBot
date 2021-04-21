import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "space_db.sqlite")


def createTable():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS data (
    id             INTEGER PRIMARY KEY AUTOINCREMENT
                           NOT NULL,
    vk_id          INTEGER UNIQUE,
    guessed_cities STRING,
    play_cities    INTEGER
);""")
    conn.commit()
    conn.close()


def getData(vk_id):
    sql = """SELECT * FROM data WHERE vk_id = ?"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql, (vk_id,))
    data = cursor.fetchall()
    conn.close()
    return data


def updateGuessedCities(guessed_cities, vk_id):
    sql = """UPDATE data SET guessed_cities = ? WHERE vk_id = ?"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql, (guessed_cities, vk_id,))
    conn.commit()
    conn.close()


def updatePlayCities(play_cities, vk_id):
    sql = """UPDATE data SET play_cities = ? WHERE vk_id = ?"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql, (play_cities, vk_id,))
    conn.commit()
    conn.close()


def updateAll(play_cities, vk_id, guessed_cities):
    sql = """INSERT INTO data(play_cities, guessed_cities, vk_id) VALUES(?, ?, ?)"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql, (play_cities, guessed_cities, vk_id,))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    pass
