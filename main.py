from fastapi import FastAPI
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


