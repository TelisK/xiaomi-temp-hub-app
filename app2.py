from lywsd03mmc import Lywsd03mmcClient
from datetime import datetime, timedelta
import time
# email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#db
import mydb
#logging
import logging
from dotenv import load_dotenv
import os
#timeout
import signal

#logging config
FORMAT = '%(asctime)s :  %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT, handlers=[logging.FileHandler('logs.log'), logging.StreamHandler()])

logger = logging.getLogger(__name__)


load_dotenv()

# Database
mydb.db_creation()
mydb.rooms_to_database()

def low_battery_email(battery, name):

    try:
        subject = 'Xiaomi Low Battery Warning'
        body = f'Your device with name "{name}", is low on battery {battery} %\nReplace the battery soon!'
        sender = os.getenv('email_sender')
        recipient = os.getenv('email_recipient')
        password = os.getenv('email_password')

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipient, msg.as_string())

        logger.warning('Low Battery Email Sent.')
        return True
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f'Email Authentication Failed. Check your Credentials : {e}')
        return False
    except ConnectionError as e:
        logger.error(f'No internet connection: {e}')
        return False
    except Exception as e:
        logger.error(f'Email not sent. Something is wrong: {e}')
        return False

def read_data(name:str, device_mac_address, timeout): # SOS must add timeout 20sec SOS  ALSO CHECK README.md AGAIN
    now_date_time = datetime.now()
    function_timeout = now_date_time + timedelta(seconds=timeout)
    while datetime.now() < function_timeout:

        try:
            room = Lywsd03mmcClient(device_mac_address)
            room_data = room.data
            
            # Database
            error_reading = 1 # 1 = True
            mydb.add_to_db(name,now_date_time.strftime('%d-%m-%Y'),now_date_time.strftime('%H:%M:%S'),room_data.temperature,room_data.humidity,room_data.battery, error_reading)
            
            logger.info(f'Rooms Name: {name} - Temperature: {str(room_data.temperature)}°C - Humidity: {str(room_data.humidity)}% - Battery: {str(room_data.battery)}%')

            if room_data.battery <= 25: # Connect with the database so can inform user every -1%.
                previous_batt = mydb.battery_lowest_check(name)

                if previous_batt is not None and previous_batt > room_data.battery:  # compare float with int
                    low_battery_email(room_data.battery, name)
                    logger.warning(f'Low Battery : {room_data.battery}%. Sending Email to user.')
                    mydb.update_battery_lowest_update(name, room_data.battery)
                    logger.info('Lowest battery cell updated')
                elif previous_batt is None:
                    mydb.update_battery_lowest_update(name, room_data.battery)
                    logger.info('Battery check skipped (No previous data)')
                elif previous_batt - room_data.battery == 0 or previous_batt < room_data.battery:
                    logger.info('Low Battery Email Not Sent - Will sent after 1% difference')
                else:
                    logger.warning('Battery check skipped (Something is wrong)')
            else:
                logger.info(f'Battery is charged')


            return str(name), str(room_data.temperature), str(room_data.humidity), str(room_data.battery)
        except Exception as e:
            error_reading = 0 # 0 = False
            logger.error(f'Connection Error at room {name} : {e}')
            return 'Error - Connection Error', {name}

    else:
        logger.error(f'Connection Timeout. Room {name} exceeded time of {timeout} seconds')
        return 'Error - Connection Timeout', {name}

while True:

    kids_bedroom = read_data('Kids',os.getenv('kids_bedroom'), timeout=2)
    parents_bedroom = read_data('Parents',os.getenv('parents_bedroom'), timeout=2)
    living_room = read_data('Living Room',os.getenv('living_room'), timeout=2)
    airbnb = read_data('Airbnb',os.getenv('airbnb'), timeout=2)


    time.sleep(300)

    