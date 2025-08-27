from pydantic import BaseModel, EmailStr, model_validator 
from typing import List, Dict

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    contact_details: Dict[str, str]
    
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age >= 60 and 'emergency' not in model.contact_details:
            raise ValueError("Emergency contact is required for patients aged 60 and above")
        return model

def patient_data_insert(patient:Patient) :
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print("Data inserted into database")

patient_data_insert(Patient(name="John Doe", age=65, email="john.doe@email.com", contact_details={"phone": "123-456-7890", "emergency": "987-654-3210"}))