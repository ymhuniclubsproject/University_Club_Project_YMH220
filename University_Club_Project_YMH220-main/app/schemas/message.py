from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel): # Schema for validating outgoing inter-club message data | Kulüpler arası giden mesaj verilerini doğrulamak için kullanılan şema
    receiver_club_id: int
    content: str

class MessageResponse(BaseModel): # Schema for returning complete message details including metadata | Üst veriler dahil tam mesaj detaylarını döndürmek için kullanılan şema
    id: int
    receiver_club_id: int
    content: str
    sender_club_id: int
    timestamp: datetime
    class Config:
        from_attributes = True # Enables Pydantic to read directly from database model instances | Pydantic'in doğrudan veri tabanı model örneklerinden okuma yapmasını sağlar

class AdminStats(BaseModel): # Schema for aggregating high-level system statistics | Üst düzey sistem istatistiklerini birleştirmek için kullanılan şema
    total_users: int
    total_clubs: int
    total_events: int