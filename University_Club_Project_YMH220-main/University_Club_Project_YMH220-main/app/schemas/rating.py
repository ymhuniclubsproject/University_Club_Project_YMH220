from pydantic import BaseModel
from typing import Optional

class RatingCreate(BaseModel): # Schema for validating new event ratings and comments | Yeni etkinlik puanlamalarını ve yorumlarını doğrulamak için kullanılan şema
    score: int
    comment: Optional[str] = None
    event_id: int

class RatingResponse(RatingCreate): # Schema for returning rating details including user and record IDs | Kullanıcı ve kayıt kimlikleri dahil puanlama detaylarını döndürmek için kullanılan şema
    id: int
    user_id: int
    class Config:
        from_attributes = True # Allows Pydantic to interface with SQLAlchemy models | Pydantic'in SQLAlchemy modelleriyle arayüz oluşturmasını sağlar