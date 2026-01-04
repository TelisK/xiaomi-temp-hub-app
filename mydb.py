import sqlite3

def db_creation():
    conn = sqlite3.connect('xiaomi-temp.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS measurements (
                measurements_id INT PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                room_id INT NOT NULL
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                temperature FLOAT NOT NULL,
                humidity FLOAT NOT NULL,
                battery FLOAT NOT NULL,
                error_reading BOOL NOT NULL,
                FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS rooms (
                id INT PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                room_name TEXT NOT NULL)''')