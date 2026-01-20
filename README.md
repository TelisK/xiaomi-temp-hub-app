
# Xiaomi Temperature Hub

A Python application to read data from multiple Xiaomi LYWSD03MMC temperature & humidity sensors and store the measurements in a local SQLite database. The app also monitors battery levels and sends email notifications when batteries are low.

---

## Features

- Read temperature, humidity, and battery from multiple Xiaomi sensors:
  - Kids Bedroom
  - Parents Bedroom
  - Living Room
  - Airbnb
- Store readings in a **SQLite database** (`xiaomi-temp-db.db`) with:
  - Rooms table
  - Measurements table (temperature, humidity, battery, battery_lowest, error tracking)
- Monitor battery levels and send **email alerts** when battery drops below 25%
- Automatically handles first-time measurements and errors during sensor reads
- Continuous monitoring loop (default: 60 seconds between cycles)

---

## Requirements

- Python 3.7+
- Libraries:
  ```bash
  pip install python-lywsd03mmc
* Email account (Gmail recommended) for battery alerts

---

## Setup

1. Clone or download the repository.
2. Update `devices.py` with your sensors' MAC addresses:

   ````python
   kids_bedroom = 'AA:BB:CC:DD:EE:FF'
   parents_bedroom = '11:22:33:44:55:66'
   living_room = '77:88:99:AA:BB:CC'
   airbnb = 'DD:EE:FF:00:11:22'
   ````
3. Update `my_accounts.py` with email credentials:

   ``````python
   email_sender = "your_email@gmail.com"
   email_recipient = "recipient_email@gmail.com"
   email_password = "your_app_password"
   ``````

   > Note: For Gmail, use an **App Password** if 2FA is enabled.
4. Run the app:

   ``````bash
   python main.py
   ``````

---

## Database Structure

* **Rooms table**

  * `id`: INTEGER PRIMARY KEY
  * `room_name`: TEXT UNIQUE NOT NULL
* **Measurements table**

  * `measurements_id`: INTEGER PRIMARY KEY AUTOINCREMENT
  * `room_id`: INTEGER (foreign key to `rooms`)
  * `measurement_date`: TEXT
  * `time`: TEXT
  * `temperature`: FLOAT
  * `humidity`: FLOAT
  * `battery`: FLOAT
  * `battery_lowest`: FLOAT
  * `error_reading`: INTEGER (1 = success, 0 = failure)

---

## How It Works

1. On startup, the app **creates the database** and **writes rooms** if they don't exist.
2. Every 60 seconds:

   * Reads data from each sensor using `Lywsd03mmcClient`.
   * Prints current readings to the console.
   * Checks battery level:

     * If battery ≤ 25% and lower than the previous value → sends email alert.
     * Updates the database with the lowest battery value.
   * Stores temperature, humidity, and battery readings in the database.
   * Logs errors if a sensor cannot be read.
3. Loop repeats indefinitely.

---

## Example Console Output

`````
--------------------
Rooms Name: Parents
Temperature: 19.64
Humidity: 64
Battery: 22
Low Battery Email Sent
--------------------
Rooms Name: Kids
Temperature: 21.32
Humidity: 60
Battery: 50
Battery is charged
`````

---

## Notes / Tips

* Ensure Bluetooth is enabled on your device running the app.
* If a sensor read fails, the error is logged and the loop continues.
* To change the monitoring interval, modify `time.sleep(60)` in `main.py`.
* Use a Gmail App Password for secure email sending.

---

## License

This project is open-source and free to use for personal or educational purposes.

