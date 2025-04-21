
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username : str
    password: str
    mobileno: Optional[str] =None
    role: Optional[str] = None
    
class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    username: str
    mobileno: Optional[str] = None
    role: Optional[str] = None
    
    class Config:
        orm_mode = True