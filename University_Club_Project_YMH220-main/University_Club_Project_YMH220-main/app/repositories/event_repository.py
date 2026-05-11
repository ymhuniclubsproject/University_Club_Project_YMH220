from sqlalchemy.orm import Session
from app.models.event import Event
from app.schemas.event import EventCreate
from datetime import datetime


class EventRepository: # Handles CRUD and filtering operations for event records | Etkinlik kayıtları için CRUD ve filtreleme işlemlerini yönetir
    @staticmethod
    def create(db: Session, event_data: EventCreate): # Persists a new event record to the database | Veri tabanına yeni bir etkinlik kaydı ekler
        db_event = Event(**event_data.model_dump())
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event

    @staticmethod
    def get_by_club(db: Session, club_id: int): # Retrieves all events organized by a specific club | Belirli bir kulüp tarafından düzenlenen tüm etkinlikleri getirir
        return db.query(Event).filter(Event.club_id == club_id).all()

    @staticmethod
    def get_past_events(db: Session): # Filters and returns events that have already taken place | Tarihi geçmiş olan etkinlikleri filtreler ve döndürür
        return db.query(Event).filter(Event.date < datetime.utcnow()).all()