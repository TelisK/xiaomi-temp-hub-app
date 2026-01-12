from lywsd03mmc import Lywsd03mmcClient
from datetime import date, time
import devices
# email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import my_accounts
#db
import mydb
import sqlite3


mydb.db_creation()

def low_battery_email(battery, name): # will connect with the database so can inform user every -1%.

    subject = 'Xiaomi Low Battery Warning'
    body = f'Your device with name "{name}", is low on battery {battery} %\nReplace the battery soon!'
    sender = my_accounts.email_sender
    recipient = my_accounts.email_recipient
    password = my_accounts.email_password

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipient, msg.as_string())
    print("Message sent!")
    return True
    

def read_data(name:str, device_mac_address):
    try:
        room = Lywsd03mmcClient(device_mac_address)
        room_data = room.data
        print(f'Rooms Name: {name},\nTemperature: {str(room_data.temperature)},\nHumidity: {str(room_data.humidity)}\nBattery: {str(room_data.battery)}')
        
        if room_data.battery <= 60:
            low_battery_email(room_data.battery, name)
            print('Low Battery Email Sent')
        else:
            print('Battery is charged')

# ------------------------------------------------------ βαση σε εξελιξη -----------------
        error_reading = 1
        mydb.add_to_db(name,date,time,room_data.temperature,room_data.humidity,room_data.battery)

        return str(name), str(room_data.temperature), str(room_data.humidity), str(room_data.battery)
    except:
        error_reading = 0
        mydb.add_to_db(name,date,time,error_reading)
        print(f'Connection Error at room {name}')
        return 'Error', {name}



while True:

    kids_bedroom = read_data('Kids',devices.kids_bedroom)
    parents_bedroom = read_data('Parents',devices.parents_bedroom)
    living_room = read_data('Living Room',devices.living_room)
    airbnb = read_data('Airbnb',devices.airbnb)



    time.sleep(60)

        