from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_user
from app.models.user import RoleEnum
from app.schemas.event import EventCreate, EventResponse
from app.repositories.event_repository import EventRepository

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/", response_model=EventResponse) # Endpoint to create new club events for authorized roles | Yetkili roller için yeni kulüp etkinlikleri oluşturma uç noktası
def create_event(event: EventCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Restricts event creation to club managers and system administrators | Etkinlik oluşturma işlemini kulüp yöneticileri ve sistem yöneticileri ile sınırlandırır
    if current_user.role not in [RoleEnum.club_manager, RoleEnum.admin]:
        raise HTTPException(status_code=403, detail="You do not have permission to create an event.")
    return EventRepository.create(db, event)

@router.get("/{club_id}", response_model=List[EventResponse]) # Fetches all events associated with a specific club | Belirli bir kulübe ait tüm etkinlikleri getirir
def get_club_events(club_id: int, db: Session = Depends(get_db)):
    return EventRepository.get_by_club(db, club_id)