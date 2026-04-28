from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.models.base import Base

class Message(Base): # Defines the schema for inter-club communication and message logs | Kulüpler arası iletişim ve mesaj kayıtları için şemayı tanımlar
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_club_id = Column(Integer, ForeignKey("clubs.id")) # Identifies the club sending the message | Mesajı gönderen kulübü tanımlar
    receiver_club_id = Column(Integer, ForeignKey("clubs.id")) # Identifies the club receiving the message | Mesajı alan kulübü tanımlar
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow) # Automatically records the UTC time of the message | Mesajın UTC zamanını otomatik olarak kaydeder