from pydantic import BaseModel
from typing import Optional


class DriverSearchObject(BaseModel):
    name:Optional[str]=None
    surname:Optional[str]=None
class ClientSearchObject(BaseModel):
    name:Optional[str]=None
    surname:Optional[str]=None
class RentSearchObject(BaseModel):
    status:Optional[str]=None

class RouteSearchObject(BaseModel):
    status:Optional[str]=None

class VehicleSearchObject(BaseModel):
    name:Optional[str]=None
    