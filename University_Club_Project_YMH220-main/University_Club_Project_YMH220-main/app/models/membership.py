from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Membership(Base): # Manages the relationship and approval status between users and clubs | Kullanıcılar ve kulüpler arasındaki ilişkiyi ve onay durumunu yönetir
    __tablename__ = "memberships"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id")) # Links the membership to a specific user | Üyeliği belirli bir kullanıcıya bağlar
    club_id = Column(Integer, ForeignKey("clubs.id")) # Links the membership to a specific club | Üyeliği belirli bir kulübe bağlar
    status = Column(String, default="pending") # Tracks the application status (pending, approved, rejected) | Başvuru durumunu takip eder (beklemede, onaylandı, reddedildi)
    club = relationship("Club", back_populates="memberships") # Enables access to club data from the membership | Üyelik üzerinden kulüp verilerine erişim sağlar
    user = relationship("User", back_populates="memberships") # Enables access to user data from the membership | Üyelik üzerinden kullanıcı verilerine erişim sağlar