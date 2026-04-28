from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.models.base import Base

class Rating(Base): # Stores event scores and feedback from users | Kullanıcılardan gelen etkinlik puanlarını ve geri bildirimlerini tutar
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer)
    comment = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id")) # Links the rating to the user who provided it | Puanı veren kullanıcıya bağlar
    event_id = Column(Integer, ForeignKey("events.id")) # Links the rating to the specific event | Puanı belirli bir etkinliğe bağlar