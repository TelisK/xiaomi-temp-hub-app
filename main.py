from fastapi import FastAPI
import mydb

app = FastAPI()

@app.get("/")
async def read_temperatures():
    data = mydb.read_data()
    rooms = []
    data_to_return = []
    for d in data:
        if d[0] not in rooms:
            data_to_return.append(d)
            rooms.append(d[0])
    return data_to_return













    # kids_bedroom = app2.read_data('Kids',devices.kids_bedroom)
    # parents_bedroom = app2.read_data('Parents',devices.parents_bedroom)
    # living_room = app2.read_data('Living Room',devices.living_room)
    # airbnb = app2.read_data('Airbnb',devices.airbnb)

    
    # return {
    #     'Kids' : kids_bedroom,
    #     'Parents' : parents_bedroom,
    #     'Living_Room' : living_room,
    #     'Airbnb' : airbnb
    # }
