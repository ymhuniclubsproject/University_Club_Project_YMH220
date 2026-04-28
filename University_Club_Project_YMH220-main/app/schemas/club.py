from pydantic import BaseModel
from typing import Optional

class ClubBase(BaseModel): # Shared attributes for club schemas | Kulüp şemaları için ortak özellikleri içerir
    name: str
    description: str

class ClubCreate(ClubBase): # Schema used for validating data during club creation | Kulüp oluşturma sırasında verileri doğrulamak için kullanılan şema
    manager_id: int

class ClubResponse(ClubBase): # Schema for returning club data including its unique ID | Benzersiz kimliği dahil kulüp verilerini döndürmek için kullanılan şema
    id: int
    manager_id: int
    class Config:
        from_attributes = True # Enables Pydantic to interface with SQLAlchemy models | Pydantic'in SQLAlchemy modelleriyle arayüz oluşturmasını sağlar