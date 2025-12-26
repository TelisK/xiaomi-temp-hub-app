from lywsd03mmc import Lywsd03mmcClient
import time
import devices

while Τrue:

    kids_bedroom = Lywsd03mmcClient(kids_bedroom)
    parents_bedroom = Lywsd03mmcClient(parents_bedroom)
    living_room = Lywsd03mmcClient(living_room)
    airbnb = Lywsd03mmcClient(airbnb)

    kids_data = kids_bedroom.data
    parents_data = parents_bedroom.data
    living_r_data = living_room.data
    airbnb_data = airbnb.data

    print('Kids Room: ')
    print('Temperature: ' + str(kids_data.temperature))
    print('Humidity: ' + str(kids_data.humidity))
    print('Battery: ' + str(kids_data.battery))
    print('Display units: ' + kids_data.units)

    print('Parents Room: ')
    print('Temperature: ' + str(parents_data.temperature))
    print('Humidity: ' + str(parents_data.humidity))
    print('Battery: ' + str(parents_data.battery))
    print('Display units: ' + parents_data.units)

    print('Living Room: ')
    print('Temperature: ' + str(living_r_data.temperature))
    print('Humidity: ' + str(living_r_data.humidity))
    print('Battery: ' + str(living_r_data.battery))
    print('Display units: ' + living_r_data.units)

    print('Airbnb House: ')
    print('Temperature: ' + str(airbnb_data.temperature))
    print('Humidity: ' + str(airbnb_data.humidity))
    print('Battery: ' + str(airbnb_data.battery))
    print('Display units: ' + airbnb_data.units)

    time.sleep(300)

# # Enable history output
# client.enable_history_progress = True

# # Retrieve the history data
# history = client.history_data

# print(history)