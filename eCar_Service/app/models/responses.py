from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserDTO(BaseModel):
    uid:str
    name: str
    surname: str
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    telephone_number: Optional[str] = None
    gender: Optional[str] = None
    registration_date: Optional[datetime] = None
    active: Optional[bool] = True

class DriverDTO(BaseModel):
    did:str
    user_id: str  
    number_of_clients_amount: Optional[int] = None
    number_of_hours_amount: Optional[int] = None
    user: UserDTO  

class ClientDTO(BaseModel):
    cid:str
    user_id: str 
    image: Optional[bytes] = None
    user: UserDTO  

class AdminDTO(BaseModel):
    aid:str
    user_id: str  
    user: UserDTO  


class RouteDTO(BaseModel):
    rid: str
    source_point_lat: Optional[float]
    source_point_lon: Optional[float]
    destination_point_lat: Optional[float]
    destination_point_lon: Optional[float]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    duration: Optional[int] = 0
    number_of_kilometers: Optional[float]=0.0
    full_price: Optional[float]=0.0
    paid: Optional[bool] = False
    status: Optional[str]
    client:Optional[ClientDTO]
    driver:Optional[DriverDTO]

class VehicleDTO(BaseModel):
    vid: str
    available: Optional[bool]
    average_fuel_consumption: Optional[float]
    name: str
    image: Optional[bytes]
    price: float

class RentDTO(BaseModel):
    rid: str
    rent_date: Optional[datetime]
    end_date: Optional[datetime]
    number_of_days: Optional[int]
    full_price: Optional[float]
    paid: Optional[bool] = False
    status: Optional[str]
    vehicle: Optional[VehicleDTO]
    client: Optional[ClientDTO]

class ReviewDTO(BaseModel):
    rid: str
    value: int
    description: str
    adding_date: Optional[datetime]=datetime.now()
    client: Optional[ClientDTO]
    driver: Optional[DriverDTO]
    route: Optional[RouteDTO]

class NotificationDTO(BaseModel):
    nid: str
    title: Optional[str]
    content: Optional[str]
    image: Optional[str] =None 
    adding_date: Optional[datetime]
    for_client: Optional[bool]

class StatisticsDTO(BaseModel):
    sid: str
    number_of_hours: Optional[int]
    number_of_clients: Optional[int]
    price_amount: Optional[float]
    beginning_of_work: Optional[datetime]
    end_of_work: Optional[datetime]
    driver: Optional[DriverDTO]

