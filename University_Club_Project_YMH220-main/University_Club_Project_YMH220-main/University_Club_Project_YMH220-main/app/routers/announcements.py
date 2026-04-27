from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_user
from app.models.user import RoleEnum
from app.schemas.announcement import AnnouncementCreate, AnnouncementResponse
from app.repositories.announcement_repository import AnnouncementRepository

router = APIRouter(prefix="/announcements", tags=["Announcements"])

@router.post("/", response_model=AnnouncementResponse)
def create_announcement(data: AnnouncementCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role not in [RoleEnum.club_manager, RoleEnum.admin]:
        raise HTTPException(status_code=403, detail="Unauthorized action")
    return AnnouncementRepository.create(db, data)

@router.get("/{club_id}", response_model=List[AnnouncementResponse])
def get_club_announcements(club_id: int, db: Session = Depends(get_db)):
    return AnnouncementRepository.get_by_club(db, club_id)