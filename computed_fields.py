from pydantic import BaseModel, computed_field
from typing import List, Dict

class Patient(BaseModel):
    name: str
    email: str
    age: int
    height: float
    weight: float
    contact_details: Dict[str, str]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
def patient_data_insert(patient:Patient) :
    print(patient.name)
    print(patient.email)
    print(patient.age) 
    print(patient.bmi)
    
    print("Data inserted into database")

patient_data_insert(Patient(name="John Doe", age=65, email="john.doe@email.com", height=1.75, weight=70.0, contact_details={"phone": "123-456-7890", "emergency": "987-654-3210"}))