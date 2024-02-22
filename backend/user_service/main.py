from fastapi import FastAPI, HTTPException
from database import collection
from users_model import BeneficiaryCreate, DonorCreate
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId

# Instance of the FastAPI application
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint to create beneficiaries
@app.post("/beneficiaries/")
async def create_beneficiary(beneficiary: BeneficiaryCreate):
    
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
@app.get("/beneficiaries/")
async def read_beneficiaries():
    try:
        # Get all beneficiaries from the MongoDB database
        beneficiaries = collection.find({"user_type": "beneficiary"})
        return {"beneficiaries": list(beneficiaries)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/beneficiaries/{beneficiary_id}")
async def read_beneficiary(beneficiary_id: str):
    try:
        # Convert the beneficiary_id to ObjectId
        beneficiary_object_id = ObjectId(beneficiary_id)
        
        # Get the beneficiary from the MongoDB database
        beneficiary = collection.find_one({"_id": beneficiary_object_id})
        
        if beneficiary is None:
            raise HTTPException(status_code=404, detail="Beneficiary not found")
        
        # Convert ObjectId to string before returning
        beneficiary["_id"] = str(beneficiary["_id"])
        
        return beneficiary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/donors/")
async def read_donors():
    # Get all donors from the MongoDB database
    try:
        donors = collection.find({"user_type": "donor"})
        return {"donors": list(donors)}  # Corrigido para usar a variável donors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/donors/{donor_id}")
async def read_donor(donor_id: str):
    try:
        # Convert the donor_id to ObjectId
        donor_object_id = ObjectId(donor_id)
        
        # Get the donor from the MongoDB database
        donor = collection.find_one({"_id": donor_object_id})
        
        if donor is None:
            raise HTTPException(status_code=404, detail="Donor not found")
        
        # Convert ObjectId to string before returning
        donor["_id"] = str(donor["_id"])
        
        return donor
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))