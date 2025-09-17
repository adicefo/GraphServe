from pydantic import BaseModel
from typing import Optional


class DriverSearchObject(BaseModel):
    name:Optional[str]=None
    surname:Optional[str]=None