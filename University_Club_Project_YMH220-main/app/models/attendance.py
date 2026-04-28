from sqlalchemy import Column, Integer, ForeignKey, Boolean
from app.models.base import Base

class Attendance(Base): # Tracks user participation status for specific events | Belirli etkinlikler için kullanıcı katılım durumunu takip eder
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id")) # Links the record to a specific user | Kaydı belirli bir kullanıcıya bağlar
    event_id = Column(Integer, ForeignKey("events.id")) # Links the record to a specific event | Kaydı belirli bir etkinliğe bağlar
    is_present = Column(Boolean, default=False) # Stores whether the user attended the event | Kullanıcının etkinliğe katılıp katılmadığını tutar