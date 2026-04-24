from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from app.core.deps import get_db
from app.services.auth_service import get_current_user
from app.models.club import Club
from app.schemas.club import ClubResponse

router = APIRouter(prefix="/search", tags=["Search & Profile"])

@router.get("/clubs", response_model=List[ClubResponse])
def search_clubs(q: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Club)
    if q:
        query = query.filter(Club.name.contains(q) | Club.description.contains(q))
    return query.all()

@router.get("/profile/{club_id}", response_model=ClubResponse)
def get_club_profile(club_id: int, db: Session = Depends(get_db)):
    return db.query(Club).filter(Club.id == club_id).first()

@router.get("/clubs", response_model=List[ClubResponse])
def search_clubs(category: Optional[str] = None, q: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Club)
    if category:
        query = query.filter(Club.category == category)
    if q:
        query = query.filter(Club.name.contains(q))
    return query.all()

@router.post("/favorite/{club_id}")
def add_favorite(club_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    club = db.query(Club).filter(Club.id == club_id).first()
    current_user.favorites.append(club)
    db.commit()
    return {"message": "Added to favorites"}

@router.get("/my-favorites", response_model=List[ClubResponse])
def get_favorites(current_user = Depends(get_current_user)):
    return current_user.favorites