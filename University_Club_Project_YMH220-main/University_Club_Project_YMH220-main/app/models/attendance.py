from sqlalchemy import Column, Integer, ForeignKey, Boolean
from app.models.base import Base

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    is_present = Column(Boolean, default=False)