import sqlite3

def db_creation():
    conn = sqlite3.connect('xiaomi-temp.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY,
                room_name TEXT UNIQUE NOT NULL)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS measurements (
                measurements_id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER NOT NULL,
                measurement_date TEXT NOT NULL,
                time TEXT NOT NULL,
                temperature FLOAT,
                humidity FLOAT,
                battery FLOAT,
                error_reading INTEGER NOT NULL,
                FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE)''')
    
    conn.commit()
    conn.close()

def rooms_to_database(): # Write the rooms to database
    rooms_to_db = {1:'Living Room',2:'Parents',3:'Kids',4:'Airbnb'}
    conn = sqlite3.connect('xiaomi-temp.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM rooms')
    exists = cur.fetchall()
    if not exists:
        for key,value in rooms_to_db.items():
            cur.execute('INSERT INTO rooms (id, room_name) VALUES (?,?)', (key,value))
        conn.commit()
        conn.close()

def add_to_db(name,measurement_date,time,temp,humid,batt,error):
    conn = sqlite3.connect('xiaomi-temp.db')
    cur = conn.cursor()
    
    cur.execute('SELECT id FROM rooms WHERE room_name = ?', (name,))
    room_id_to_db = cur.fetchone()[0]

    cur.execute('INSERT INTO measurements (room_id,measurement_date,time,temperature,humidity,battery,error_reading) VALUES (?,?,?,?,?,?,?)',
                (room_id_to_db,
                measurement_date,
                time,
                temp,
                humid,
                batt,
                error)
                )
    conn.commit()
    conn.close()
    

def add_to_db_error(name,measurement_date,time,error):
    conn = sqlite3.connect('xiaomi-temp.db')
    cur = conn.cursor()
    
    cur.execute('SELECT id FROM rooms WHERE room_name = ?', (name,))
    room_id_to_db = cur.fetchone()[0]

    cur.execute('INSERT INTO measurements (room_id,measurement_date,time,error_reading) VALUES (?,?,?,?)', (
        room_id_to_db,
        measurement_date,
        time,
        error
    ))
    conn.commit()
    conn.close()

def battery_fall_check(name): # Checking the last value of the battery on the database
    conn = sqlite3.connect('xiaomi-temp.db')
    cur = conn.cursor()

    cur.execute('SELECT id FROM rooms WHERE room_name = ?', (name,))
    room_id_to_check = cur.fetchone()[0]

    cur.execute('SELECT battery FROM measurements WHERE room_id = ? AND battery IS NOT NULL ORDER BY measurements_id DESC LIMIT 1', (room_id_to_check,))
    previous_batt_measurement = cur.fetchone()[0]
    return previous_batt_measurement
    