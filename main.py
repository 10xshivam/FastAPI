from fastapi import FastAPI,Path,HTTPException,Query
import json

app = FastAPI()

def loadData():
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data


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