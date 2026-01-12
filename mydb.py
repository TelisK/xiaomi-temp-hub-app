import sqlite3

def db_creation():
    conn = sqlite3.connect('xiaomi-temp.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_name TEXT NOT NULL)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS measurements (
                measurements_id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER NOT NULL
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                temperature FLOAT NOT NULL,
                humidity FLOAT NOT NULL,
                battery FLOAT NOT NULL,
                error_reading INTEGER NOT NULL,
                FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE)''')
    
    conn.commit()

def add_to_db(name,date,temp,humid,batt):
    conn = sqlite3.connect('xiaomi-temp.db')
    cur = conn.cursor()
    
    cur.execute('INSERT INTO rooms (room_name) VALUES (?)', str(name))
    cur.execute('INSERT INTO measurements ()')