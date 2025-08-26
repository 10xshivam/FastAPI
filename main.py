from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API for managing patient data."}


