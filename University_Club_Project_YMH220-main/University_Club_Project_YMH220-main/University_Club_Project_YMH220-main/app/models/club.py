from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Club(Base):
    __tablename__ = "clubs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    category = Column(String, default="Genel")
    manager_id = Column(Integer, ForeignKey("users.id"))
    
    manager = relationship("User", back_populates="managed_clubs")
    events = relationship("Event", back_populates="club")
    memberships = relationship("Membership", back_populates="club")