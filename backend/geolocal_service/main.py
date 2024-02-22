from fastapi import FastAPI, Depends, HTTPException
from typing import Optional
from database import Database
from geolocation import Geolocation

app = FastAPI()
database = Database()
geolocation = Geolocation()

@app.get("/users/distance/")
async def calculate_distance(beneficiary_id: str, donor_id: str):
    beneficiary_address = database.get_address(beneficiary_id)
    donor_address = database.get_address(donor_id)

    if not beneficiary_address or not donor_address:
        raise HTTPException(status_code=404, detail="Address not found")

    distance = geolocation.calculate_distance(beneficiary_address, donor_address)
    return {"distance": distance}