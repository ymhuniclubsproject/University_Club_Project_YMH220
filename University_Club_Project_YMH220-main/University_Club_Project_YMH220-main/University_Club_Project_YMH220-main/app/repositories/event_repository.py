from sqlalchemy.orm import Session
from app.models.event import Event
from app.schemas.event import EventCreate
from datetime import datetime



class EventRepository:
    @staticmethod
    def create(db: Session, event_data: EventCreate):
        db_event = Event(**event_data.model_dump())
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event

    @staticmethod
    def get_by_club(db: Session, club_id: int):
        return db.query(Event).filter(Event.club_id == club_id).all()

    @staticmethod
    def get_past_events(db: Session):
        return db.query(Event).filter(Event.date < datetime.utcnow()).all()