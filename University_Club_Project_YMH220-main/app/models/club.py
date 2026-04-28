from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Club(Base): # Defines the core club model with relationships to managers, events, and members | Kulüp modelini; yönetici, etkinlik ve üyelik ilişkileriyle tanımlar
    __tablename__ = "clubs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    category = Column(String, default="Genel")
    manager_id = Column(Integer, ForeignKey("users.id")) # Links the club to its responsible manager | Kulübü sorumlu yöneticisine bağlar
    
    manager = relationship("User", back_populates="managed_clubs") # Defines the link back to the User model | User modeline geri dönüş ilişkisini tanımlar
    events = relationship("Event", back_populates="club") # Accesses all events associated with this club | Bu kulübe ait tüm etkinliklere erişim sağlar
    memberships = relationship("Membership", back_populates="club") # Manages the list of club members | Kulüp üyeleri listesini yönetir