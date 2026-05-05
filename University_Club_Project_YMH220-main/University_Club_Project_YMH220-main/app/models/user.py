from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum
from app.core.database import Base

class RoleEnum(str, enum.Enum): # Defines available user access levels in the system | Sistemdeki mevcut kullanıcı erişim seviyelerini tanımlar
    student = "student"
    club_manager = "club_manager"
    admin = "admin"

user_favorites = Table( # Association table for the many-to-many relationship between users and favorite clubs | Kullanıcılar ve favori kulüpler arasındaki çoktan çoğa ilişki tablosu
    'user_favorites', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('club_id', Integer, ForeignKey('clubs.id'), primary_key=True)
)

class User(Base): # Central user model handling authentication, roles, and relational links | Kimlik doğrulama, roller ve ilişkisel bağlantıları yöneten temel kullanıcı modeli
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.student, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    managed_clubs = relationship("Club", back_populates="manager") # Links to clubs specifically managed by this user | Bu kullanıcı tarafından yönetilen kulüplere bağlanır
    memberships = relationship("Membership", back_populates="user") # Accesses all club membership records for the user | Kullanıcının tüm kulüp üyelik kayıtlarına erişim sağlar
    favorites = relationship("Club", secondary=user_favorites) # Manages the collection of clubs marked as favorites | Favori olarak işaretlenen kulüpler koleksiyonunu yönetir