from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=100, title="Full Name", description="The patient's full name")]
    email: EmailStr
    linkedin: AnyUrl
    age: int = Field(..., gt=0, description="Age must be a positive integer")
    weight: Annotated[float, Field(gt=0, strict=True, description="Weight must be a positive number")]
    married: Annotated[bool, Field(title="Marital Status", description="Indicates if the patient is married")]
    allergies: Annotated[Optional[List[str]], Field(default=None, title="Allergies", description="List of allergies the patient has")]
    contact_info: Dict[str,str]

def patient_data_insert(patient:Patient) :
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_info)
    print("Data inserted into database")

patient_data_insert(Patient(name="John Doe", age=30, weight=70.5, email="john.doe@example.com", married=False, linkedin="https://www.linkedin.com/in/johndoe/", contact_info={"email": "john.doe@example.com", "phone": "123-456-7890"}))

