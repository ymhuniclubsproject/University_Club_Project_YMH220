from pydantic import BaseModel
from typing import Optional

class ClubBase(BaseModel):
    name: str
    description: str

class ClubCreate(ClubBase):
    manager_id: int

class ClubResponse(ClubBase):
    id: int
    manager_id: int
    class Config:
        from_attributes = True