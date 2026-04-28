from sqlalchemy.orm import Session
from app.models.announcement import Announcement
from app.schemas.announcement import AnnouncementCreate

class AnnouncementRepository: # Handles database operations for announcement records | Duyuru kayıtları için veri tabanı işlemlerini yönetir
    @staticmethod
    def create(db: Session, data: AnnouncementCreate): # Persists a new announcement to the database | Yeni bir duyuruyu veri tabanına kaydeder
        db_obj = Announcement(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def get_by_club(db: Session, club_id: int): # Retrieves all announcements linked to a specific club | Belirli bir kulübe bağlı tüm duyuruları getirir
        return db.query(Announcement).filter(Announcement.club_id == club_id).all()