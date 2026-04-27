from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db
from app.schemas.event import EventResponse
from app.repositories.event_repository import EventRepository

router = APIRouter(prefix="/archive", tags=["Archive"])

@router.get("/events", response_model=List[EventResponse])
def get_past_events(db: Session = Depends(get_db)):
    return EventRepository.get_past_events(db)