from pydantic import BaseModel, EmailStr, AnyUrl, field_validator
from typing import List, Dict

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    contact_details: Dict[str, str]

    # We want only icici and hdfc email domains
    @field_validator('email')
    @classmethod
    def email_validator(cls, value ):
        valid_domains = ['hdfc.com', 'icici.com']
        domains_name = value.split('@')[-1]
        if domains_name not in valid_domains:
            raise ValueError(f"Email domain '{domains_name}' is not allowed")
        return value

    # We want name should be capitalized
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    # validator types
    @field_validator('age', mode='after')
    @classmethod
    def age_validator(cls, value):
        if value < 0:
            raise ValueError("Age must be a positive integer")
        return value

    # If we want to validate on two fields like age and contact details like if patient age is 60+ then its should have one emergency number, we cannot do it with field_validator

def patient_data_insert(patient:Patient) :
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print("Data inserted into database")

# Validator works on two modes after and before, by default after
# after -> email will be validated after type checking
# before -> email will be validated before type checking
patient_data_insert(Patient(name="John Doe", age='30', email="john.doe@icici.com"))
