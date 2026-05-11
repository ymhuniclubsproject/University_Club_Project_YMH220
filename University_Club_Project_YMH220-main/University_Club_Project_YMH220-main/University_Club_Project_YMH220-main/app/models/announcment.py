from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.models.base import Base

class Announcement(Base):
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    club_id = Column(Integer, ForeignKey("clubs.id"))