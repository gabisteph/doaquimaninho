from fastapi import FastAPI, HTTPException
from database import collection
from users_model import BeneficiaryCreate, DonorCreate

# Instance of the FastAPI application
app = FastAPI()

# Endpoint to create beneficiaries
@app.post("/beneficiaries/")
async def create_beneficiary(beneficiary: BeneficiaryCreate):
    # Check if the beneficiary type is valid
    if beneficiary.beneficiaryType not in ['person', 'institution']:
        raise HTTPException(status_code=400, detail="Invalid beneficiary type. Must be 'person' or 'institution'.")

    # Insert the beneficiary into the MongoDB database
    try:
        result = collection.insert_one(beneficiary.dict())
        if result.inserted_id:
            return {"message": "Beneficiary created successfully", "beneficiary_id": str(result.inserted_id)}
        else:
            raise HTTPException(status_code=500, detail="Failed to create beneficiary.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to create donors
@app.post("/donors/")
async def create_donor(donor: DonorCreate):
    # Insert the donor into the MongoDB database
    try:
        result = collection.insert_one(donor.dict())
        if result.inserted_id:
            return {"message": "Donor created successfully", "donor_id": str(result.inserted_id)}
        else:
            raise HTTPException(status_code=500, detail="Failed to create donor.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
