from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    receiver_club_id: int
    content: str

class MessageResponse(BaseModel):
    id: int
    receiver_club_id: int
    content: str
    sender_club_id: int
    timestamp: datetime
    class Config:
        from_attributes = True

class AdminStats(BaseModel):
    total_users: int
    total_clubs: int
    total_events: int