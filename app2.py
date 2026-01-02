from lywsd03mmc import Lywsd03mmcClient
import time
import devices


def read_data(name:str, device_mac_address):
    try:
        room = Lywsd03mmcClient(device_mac_address)
        room_data = room.data
        print(f'Rooms Name: {name},\nTemperature: {str(room_data.temperature)},\nHumidity: {str(room_data.humidity)}\nBattery: {str(room_data.battery)}')
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

        



'''while True:

    kids_bedroom = Lywsd03mmcClient(devices.kids_bedroom)
    parents_bedroom = Lywsd03mmcClient(devices.parents_bedroom)
    living_room = Lywsd03mmcClient(devices.living_room)
    airbnb = Lywsd03mmcClient(devices.airbnb)

    kids_data = kids_bedroom.data
    parents_data = parents_bedroom.data
    living_r_data = living_room.data
    airbnb_data = airbnb.data

    print('Kids Room: ')
    print('Temperature: ' + str(kids_data.temperature))
    print('Humidity: ' + str(kids_data.humidity))
    print('Battery: ' + str(kids_data.battery))
    #print('Display units: ' + kids_data.units)

    print('Parents Room: ')
    print('Temperature: ' + str(parents_data.temperature))
    print('Humidity: ' + str(parents_data.humidity))
    print('Battery: ' + str(parents_data.battery))
    # print('Display units: ' + parents_data.units)

    print('Living Room: ')
    print('Temperature: ' + str(living_r_data.temperature))
    print('Humidity: ' + str(living_r_data.humidity))
    print('Battery: ' + str(living_r_data.battery))
    # print('Display units: ' + living_r_data.units)

    print('Airbnb House: ')
    print('Temperature: ' + str(airbnb_data.temperature))
    print('Humidity: ' + str(airbnb_data.humidity))
    print('Battery: ' + str(airbnb_data.battery))
    # print('Display units: ' + airbnb_data.units)

    time.sleep(300)

# # Enable history output
# client.enable_history_progress = True

# # Retrieve the history data
# history = client.history_data

# print(history)'''