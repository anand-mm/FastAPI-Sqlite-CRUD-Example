from typing import Optional
from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    
class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int 
    
    class Config:
        orm_mode = True