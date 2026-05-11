from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db
from app.schemas.event import EventResponse
from app.repositories.event_repository import EventRepository

router = APIRouter(prefix="/archive", tags=["Archive"])

@router.get("/events", response_model=List[EventResponse]) # Endpoint to retrieve events that have already concluded | Tamamlanmış etkinlikleri getirmek için uç nokta
def get_past_events(db: Session = Depends(get_db)): # Fetches the list of past events from the repository | Arşivdeki geçmiş etkinlik listesini depodan çeker
    return EventRepository.get_past_events(db)