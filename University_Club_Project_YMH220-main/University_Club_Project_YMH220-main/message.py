from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel): # Validation schema for sending messages | Mesaj gönderimi için doğrulama şeması
    receiver_club_id: int
    content: str

class MessageResponse(BaseModel): # Schema for returning message data | Mesaj verilerini döndürme şeması
    id: int
    receiver_club_id: int
    content: str
    sender_club_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True # Enables ORM object compatibility | ORM nesneleriyle uyumluluk sağlar