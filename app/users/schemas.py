
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExpoLoginBase(BaseModel):
    loginid: str
    usertype: str
    createdby: Optional[int] = None
    
class UserCreate(ExpoLoginBase):
    password: str

class UserResponse(ExpoLoginBase):
    id: int
    loginid: str
    usertype: str
    createddate: datetime   
    
    class Config:
        from_attributes = True