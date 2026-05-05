from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.models.base import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    sender_club_id = Column(Integer, ForeignKey("clubs.id"))
    receiver_club_id = Column(Integer, ForeignKey("clubs.id"))
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)