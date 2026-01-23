from lywsd03mmc import Lywsd03mmcClient
from datetime import datetime
import time
import devices
# email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import my_accounts
#db
import mydb



mydb.db_creation()
mydb.rooms_to_database()

def low_battery_email(battery, name):

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
    now_date_time = datetime.now()
    try:
        room = Lywsd03mmcClient(device_mac_address)
        room_data = room.data
        print('--------------------')
        print(f'Rooms Name: {name}\nTemperature: {str(room_data.temperature)}\nHumidity: {str(room_data.humidity)}\nBattery: {str(room_data.battery)}')
        
        if room_data.battery <= 25: # Connect with the database so can inform user every -1%.
            previous_batt = mydb.battery_lowest_check(name)
            if previous_batt is not None and previous_batt > room_data.battery:  # compare float with int
                low_battery_email(room_data.battery, name)
                print('Low Battery Email Sent')
                mydb.update_battery_lowest_update(name, room_data.battery)
            elif previous_batt is None:
                mydb.update_battery_lowest_update(name, room_data.battery)
                print('Battery check skipped (No previous data)')
            elif previous_batt - room_data.battery == 0 or previous_batt < room_data.battery:
                print('Low Battery Email Not Sent - Will sent after 1%% difference')
            else:
                print('Battery check skipped (Something is wrong)')
        else:
            print('Battery is charged')

# Database
        error_reading = 1 # 1 = True
        mydb.add_to_db(name,now_date_time.strftime('%d-%m-%Y'),now_date_time.strftime('%H:%M:%S'),room_data.temperature,room_data.humidity,room_data.battery, error_reading)

        return str(name), str(room_data.temperature), str(room_data.humidity), str(room_data.battery)
    except:
        error_reading = 0 # 0 = False
        #mydb.add_to_db_error(name,now_date_time.strftime('%d-%m-%Y'),now_date_time.strftime('%H:%M:%S'),error_reading)
        print('--------------------')
        print(f'Connection Error at room {name}')
        return 'Error', {name}



while True:

    kids_bedroom = read_data('Kids',devices.kids_bedroom)
    parents_bedroom = read_data('Parents',devices.parents_bedroom)
    living_room = read_data('Living Room',devices.living_room)
    airbnb = read_data('Airbnb',devices.airbnb)



    time.sleep(300)

    