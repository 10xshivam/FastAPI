from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field   
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="The unique identifier for the patient",example="P001")]
    name: Annotated[str, Field(..., description="The name of the patient", example="John Doe")]
    city: Annotated[str, Field(..., description="The city where the patient resides", example="New York")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="The age of the patient", ge=0)]
    gender: Annotated[Literal["Male", "Female", "Other"], Field(..., description="The gender of the patient", example="Male")]
    height: Annotated[float, Field(..., description="The height of the patient in meters", gt=0)]
    weight: Annotated[float, Field(..., description="The weight of the patient in kilograms", gt=0)]

    @computed_field
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

def loadData():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data

def saveData(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API for managing patient data."}

@app.get("/view")
def view():
    data = loadData()
    return data

# Path Parameters
@app.get("/view/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="P001")):
    data = loadData()
    if patient_id in data :
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found.")

# Query Parameters
@app.get("/sort")
def sort_patients(sort_by:str = Query(...,description='Sort on the basis of height,weight or bmi'),order: str = Query('asc',description='Sort in ascending or descending order, default is ascending')):

    valid_fields = ['height', 'weight', 'bmi']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by field. Must be one of {valid_fields}.")
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order field. Must be 'asc' or 'desc'.")
    
    data = loadData()
    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by,  0), reverse=sort_order)

    return sorted_data

@app.post("/create")
def create_patient(patient: Patient):
    # Load existing data
    data = loadData()
    
    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists.")

    # Add the new patient to the data
    data[patient.id] = patient.model_dump(exclude=['id']) # convert pydantic object to dict 
    saveData(data)

    return JSONResponse(status_code=201, content={"message": "Patient created successfully.", "patient": data[patient.id]})