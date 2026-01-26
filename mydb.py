import sqlite3

def db_creation():
    with sqlite3.connect('xiaomi-temp-db.db') as conn:
        cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY,
                room_name TEXT UNIQUE NOT NULL,
                battery_lowest FLOAT)''')
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

def rooms_to_database(): # Write the rooms to database
    rooms_to_db = {1:'Living Room',2:'Parents',3:'Kids',4:'Airbnb'}
    with sqlite3.connect('xiaomi-temp-db.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM rooms')
        exists = cur.fetchall()
        if not exists:
            for key,value in rooms_to_db.items():
                cur.execute('INSERT INTO rooms (id, room_name) VALUES (?,?)', (key,value))

def add_to_db(name,measurement_date,time,temp,humid,batt,error):
    with sqlite3.connect('xiaomi-temp-db.db') as conn:
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
    
def battery_lowest_check(name):
    with sqlite3.connect('xiaomi-temp-db.db') as conn:
        cur = conn.cursor()

        cur.execute('SELECT battery_lowest FROM rooms WHERE room_name = ?', (name,))
        battery_lowest_value = cur.fetchone()
        return battery_lowest_value[0] if battery_lowest_value is not None else None

def update_battery_lowest_update(name, battery):
    with sqlite3.connect('xiaomi-temp-db.db') as conn:  # database must close after return
        cur = conn.cursor()

        cur.execute('UPDATE rooms SET battery_lowest = ? WHERE room_name = ?', (battery,name))
        print('Lowest battery cell updated')

def read_data():
    with sqlite3.connect('xiaomi-temp-db.db') as conn:
        cur = conn.cursor()

        cur.execute('SELECT rooms.room_name, rooms.battery_lowest, measurements.measurement_date, measurements.time, ' \
        'measurements.temperature, measurements.humidity, measurements.battery ' \
        'FROM rooms LEFT JOIN measurements ON rooms.id = measurements.room_id ORDER BY measurements.measurement_date DESC, measurements.time DESC ')

        data = cur.fetchall()
        return data