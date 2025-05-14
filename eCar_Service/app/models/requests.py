from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class UserInsertRequest(BaseModel):
    name: str
    surname: str
    username: Optional[str] = None
    email: EmailStr
    password: str
    passwordConfirm: str
    telephoneNumber: Optional[str] = None
    gender: Optional[str] = None
    isActive: Optional[bool] = True

    class Config:
        min_anystr_length = 1
        anystr_strip_whitespace = True
