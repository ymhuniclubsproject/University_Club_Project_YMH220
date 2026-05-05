from pydantic import BaseModel
from datetime import datetime

class EventBase(BaseModel): # Shared attributes representing the core data of an event | Bir etkinliğin temel verilerini temsil eden ortak özellikler
    title: str
    description: str
    date: datetime
    location: str
    club_id: int

class EventCreate(EventBase): # Schema used for validating data during event creation | Etkinlik oluşturma sırasında verileri doğrulamak için kullanılan şema
    pass

class EventResponse(EventBase): # Schema for returning event details including the unique database ID | Benzersiz veri tabanı kimliği dahil etkinlik detaylarını döndürmek için şema
    id: int

    class Config:
        from_attributes = True # Enables mapping from ORM objects to Pydantic models | ORM nesnelerinden Pydantic modellerine eşlemeyi sağlar