from sqlalchemy.orm import Session
from app.models.announcement import Announcement
from app.schemas.announcement import AnnouncementCreate

class AnnouncementRepository:
    @staticmethod
    def create(db: Session, data: AnnouncementCreate):
        db_obj = Announcement(**data.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def get_by_club(db: Session, club_id: int):
        return db.query(Announcement).filter(Announcement.club_id == club_id).all()