from fastapi import FastAPI
import app2
import devices

import mydb

app = FastAPI()

@app.get("/")
async def read_temperatures():
    kids_bedroom = app2.read_data('Kids',devices.kids_bedroom)
    parents_bedroom = app2.read_data('Parents',devices.parents_bedroom)
    living_room = app2.read_data('Living Room',devices.living_room)
    airbnb = app2.read_data('Airbnb',devices.airbnb)

    
    return {
        'Kids' : kids_bedroom,
        'Parents' : parents_bedroom,
        'Living_Room' : living_room,
        'Airbnb' : airbnb
    }

@app.get("/read_temp_db")
async def read_temperatures_db():
    pass