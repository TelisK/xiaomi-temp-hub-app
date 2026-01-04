from lywsd03mmc import Lywsd03mmcClient
import time
import devices
# email
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import accounts


def low_battery_email(battery, name): # will connect with the database so can inform user every -1%.
    msg = MIMEMultipart()
    msg['From'] = accounts.email_username
    msg['To'] = 'telis.koutsogiannakis@gmail.com'
    msg['Subject'] = 'Xiaomi Low Battery Warning'
    message = f'Your device with name "{name}", is low on battery {battery} %\nReplace the battery soon!'
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttils()
    mailserver.ehlo()
    mailserver.login(accounts.email_username, accounts.email_password) 
    mailserver.sendmail(accounts.email_username,accounts.email_receiver,msg.as_string())
    mailserver.quit()
    

def read_data(name:str, device_mac_address):
    try:
        room = Lywsd03mmcClient(device_mac_address)
        room_data = room.data
        print(f'Rooms Name: {name},\nTemperature: {str(room_data.temperature)},\nHumidity: {str(room_data.humidity)}\nBattery: {str(room_data.battery)}')
        
        if int(room_data.battery) <= 50:
            low_battery_email(room_data.battery, name)

        return str(name), str(room_data.temperature), str(room_data.humidity), str(room_data.battery)
    except:
        print(f'Connection Error at room {name}')
        return 'Error', {name}



while True:

    kids_bedroom = read_data('Kids',devices.kids_bedroom)
    parents_bedroom = read_data('Parents',devices.parents_bedroom)
    living_room = read_data('Living Room',devices.living_room)
    airbnb = read_data('Airbnb',devices.airbnb)



    time.sleep(60)

        