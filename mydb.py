import sqlite3

def db_creation():
    conn = sqlite3.connect('xiaomi-temp.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY,
                room_name TEXT UNIQUE NOT NULL)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS measurements (
                measurements_id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER NOT NULL
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                temperature FLOAT,
                humidity FLOAT,
                battery FLOAT,
                error_reading INTEGER NOT NULL,
                FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE)''')
    
    conn.commit()

#write the rooms to database
rooms_to_db = {1:'living_room',2:'parents_bedroom',3:'kids_bedroom',4:'airbnb'}
conn = sqlite3.connect('xiaomi-temp.db')
cur = conn.cursor()
for key,value in rooms_to_db.items():
    cur.execute('INSERT INTO rooms (id, room_name) VALUES (?,?)', (key,value))


def add_to_db(name,date,time,temp,humid,batt,error):
    conn = sqlite3.connect('xiaomi-temp.db')
    cur = conn.cursor()
    
    cur.execute('SELECT id FROM rooms WHERE room_name = ?', name)
    room_id_to_db = cur.fetchall()[0]

    cur.execute('INSERT INTO measurements (room_id,date,time,temperature,humidity,battery,error_reading) VALUES (?,?,?,?,?,?,?)',
                (room_id_to_db,
                date,
                time,
                temp,
                humid,
                batt,
                error)
                )

def add_to_db_error(name,date,time,error):
    conn = sqlite3.connect('xiaomi-temp.db')
    cur = conn.cursor()
    
    cur.execute('SELECT id FROM rooms WHERE room_name = ?', name)
    room_id_to_db = cur.fetchall()[0]

    cur.execute('INSERT INTO measurements (room_id,date,time,error_reading) VALUES (?,?,?,?)', (
        room_id_to_db,
        date,
        time,
        error
    ))
    