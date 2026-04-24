from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.club import Club
from app.schemas.club import ClubCreate

class ClubRepository:
    @staticmethod
    def create(db: Session, club_data: ClubCreate):
        existing_club = db.query(Club).filter(Club.name == club_data.name).first()
        if existing_club:
            raise HTTPException(status_code=400, detail="A club with this name already exists.")
            
        db_club = Club(**club_data.model_dump())
        db.add(db_club)
        db.commit()
        db.refresh(db_club)
        return db_club

    @staticmethod
    def get_all(db: Session):
        return db.query(Club).all()

    @staticmethod
    def get_by_id(db: Session, club_id: int):
        return db.query(Club).filter(Club.id == club_id).first()