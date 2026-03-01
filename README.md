# Xiaomi Temperature Hub

A Python application to read data from multiple Xiaomi LYWSD03MMC temperature & humidity sensors and store the measurements in a local SQLite database. The app also monitors battery levels and sends email notifications when batteries are low.

---

## Features

- Read temperature, humidity, and battery from multiple Xiaomi sensors:
  - Kids Bedroom
  - Parents Bedroom
  - Living Room
  - Airbnb
- Store readings in a **SQLite database** with a Rooms table and Measurements table
- Monitor battery levels and send **email alerts** when battery drops below 25%
- Connection timeout protection (default: 20 seconds per device)
- Full logging to terminal and `logs.log` file

---

## Requirements

- Python 3.7+
- Raspberry Pi with Bluetooth enabled

```bash
pip install python-lywsd03mmc python-dotenv pebble
```

- Email account (Gmail recommended) for battery alerts

---

## Setup

1. Clone or download the repository.

2. Create a `.env` file in the root folder with your credentials and MAC addresses:

```env
# Email
email_sender=yourmail@gmail.com
email_password=your_app_password
email_recipient=recipient@gmail.com

# Device MAC Addresses
kids_bedroom=A4:C1:38:XX:XX:XX
parents_bedroom=A4:C1:38:XX:XX:XX
living_room=A4:C1:38:XX:XX:XX
airbnb=A4:C1:38:XX:XX:XX
```

>  For Gmail, use an **App Password** if 2FA is enabled.

3. Run the app:

```bash
python main.py
```

---

## Database Structure

**Rooms table** — `id`, `room_name`

**Measurements table** — `measurements_id`, `room_id`, `measurement_date`, `time`, `temperature`, `humidity`, `battery`, `battery_lowest`

---

## How It Works

1. On startup, the app creates the database and writes rooms if they don't exist.
2. Every 5 minutes:
   - Reads data from each sensor with a 20-second timeout per device.
   - Checks battery level — if battery ≤ 25% and lower than previous value, sends email alert.
   - Stores all readings in the database.
   - Logs errors if a sensor cannot be read.
3. Loop repeats indefinitely.

---

## Notes

- BLE connections are sequential due to single Bluetooth adapter limitations.
- To change the monitoring interval, modify `time.sleep(300)` in `main.py`.
- Logs are written to both the terminal and `logs.log`.

---

## License

This project is open-source and free to use for personal or educational purposes.
