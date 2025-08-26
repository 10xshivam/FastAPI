from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class Patient(BaseModel):
    name: str
    email: str
    age: int = 20
    height: float
    weight: float
    contact_details: dict[str, str]
    address: Address

address1 = Address(street="123 Main St", city="Anytown", state="CA", zip_code="12345")

patient1 = Patient(name="John Doe", email="john.doe@email.com", age=30, height=1.75, weight=70.0, contact_details={"phone": "123-456-7890"}, address=address1)

# print(patient1.address.city) 

# Convert to dictionary
# temp = patient1.model_dump()
temp = patient1.model_dump(include=['age', 'name']) # export ke time pr sirf ye do fields chahiye
temp = patient1.model_dump(exclude={'address':['state']}) # address se state field ko exclude kiya

temp = patient1.model_dump(exclude_unset=True) # jo fields set nhi kiye gay during object creation unko exclude kar dega

print(temp)
print(type(temp))

# Convert to dictionary
temp2 = patient1.model_dump_json()
print(temp2)
print(type(temp2))