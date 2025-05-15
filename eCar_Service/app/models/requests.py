from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional
import re,datetime
from fastapi import HTTPException

class UserInsertRequest(BaseModel):
    name: str
    surname: str
    username: Optional[str] = None
    email: EmailStr
    password: str
    password_conifrm: str
    telephone_number: Optional[str] = None
    gender: Optional[str] = None
    active: Optional[bool] = True

    @field_validator('name', 'surname')
    @classmethod
    def capitalize_first_letter(cls, v: str):
        if not v or not v[0].isupper():
            raise ValueError('Must start with a capital letter')
        return v

    @field_validator('username')
    @classmethod
    def username_min_length(cls, v: Optional[str]):
        if v is not None and len(v) < 5:
            raise ValueError('Username must be at least 5 characters long')
        return v

    @field_validator('telephone_number')
    @classmethod
    def validate_telephone_format(cls, v: Optional[str]):
        if v is not None:
            pattern = r"^06\d-\d{3}-\d{3,4}$"
            if not re.match(pattern, v):
                raise ValueError('Telephone number must be in format 06x-xxx-xxx(x)')
        return v
    
    @field_validator("email")
    @classmethod
    def validate_email(cls,v:Optional[str]):
        if v is not None:
            pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,6}(\\,[a-zA-Z]{2,6})?$"
            if not re.match(pattern,v):
                raise ValueError('Email must be in format name(.surname)@example.com')
        return v
    @field_validator("gender")
    @classmethod
    def validate_email(cls,v:Optional[str]):
        if v is not None:
            pattern=r"^(male|female|Male|Female)$"
            if not re.match(pattern,v):
                raise ValueError('Gender must be either male|female|Male|Female')
        return v
    
class RouteInsertRequest(BaseModel):
    source_point_lat: float
    source_point_lon: float
    destination_point_lat: float
    destination_point_lon: float
    client_id: str
    driver_id: str

    @field_validator('source_point_lat', 'destination_point_lat')
    @classmethod
    def min_max_values_latitudes(cls, value: float):
        if value is not  None and  (value<=-90 or value>=90):
            raise ValueError('Latitude must be between -90 and 90 degrees')
        return value

    @field_validator('source_point_lon','destination_point_lon')
    @classmethod
    def min_max_values_longitudes(cls, value: float):
        if value is not None and (value<=-180 or value>=180):
            raise ValueError('Longitude must be between -180 and 180 degrees')
        return value

class VehicleInsertRequest(BaseModel):
    name:str
    available:bool
    average_fuel_consumption:float
    image:Optional[str]=None
    price:float

    @field_validator('average_fuel_consumption')
    @classmethod
    def min_max_fuel_consumption(cls, value: float):
            if value is not  None and  (value<=3 or value>=18):
                raise ValueError('Please insert valid fuel consumption')
            return value

    @field_validator('price')
    @classmethod
    def min_max_price(cls, value: float):
        if value is not None and (value<40 or value>65):
            raise ValueError('Price must be in range from 40 to 65')
        return value
class RentInsertRequest(BaseModel):
    rent_date: datetime.datetime
    end_date: datetime.datetime
    vehicle_id: str
    client_id: str

    @model_validator(mode="after")
    def validate_dates(cls, values):
        if values.end_date <= values.rent_date:
            raise ValueError("End date must be after rent date")
        return values
