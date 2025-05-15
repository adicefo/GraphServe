from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserDTO(BaseModel):
    name: str
    surname: str
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    telephone_number: Optional[str] = None
    gender: Optional[str] = None
    registration_date: Optional[datetime] = None
    active: Optional[bool] = True

class DriverDTO(BaseModel):
    user_id: str  
    number_of_clients_amount: Optional[int] = None
    number_of_hours_amount: Optional[int] = None
    user: UserDTO  

class ClientDTO(BaseModel):
    user_id: str 
    image: Optional[bytes] = None
    user: UserDTO  

class AdminDTO(BaseModel):
    user_id: str  
    user: UserDTO  
