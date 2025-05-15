from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional
import re

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