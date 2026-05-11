from pydantic import BaseModel
from datetime import datetime

class AnnouncementCreate(BaseModel): # Schema for validating incoming announcement data | Gelen duyuru verilerini doğrulamak için kullanılan şema
    title: str
    content: str
    club_id: int

class AnnouncementResponse(AnnouncementCreate): # Schema for outgoing announcement data including database-generated fields | Veri tabanı tarafından oluşturulan alanları içeren giden veri şeması
    id: int
    created_at: datetime
    class Config:
        from_attributes = True # Enables compatibility with ORM models | ORM modelleri ile uyumluluğu sağlar