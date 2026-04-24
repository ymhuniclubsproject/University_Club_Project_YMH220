from pydantic import BaseModel
from typing import Optional

class RatingCreate(BaseModel):
    score: int
    comment: Optional[str] = None
    event_id: int

class RatingResponse(RatingCreate):
    id: int
    user_id: int
    class Config:
        from_attributes = True