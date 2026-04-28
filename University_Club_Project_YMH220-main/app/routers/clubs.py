from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.schemas.club import ClubCreate, ClubResponse
from app.repositories.club_repository import ClubRepository

router = APIRouter(prefix="/clubs", tags=["Clubs"])

@router.post("/", response_model=ClubResponse) # Restricts new club creation to system administrators | Yeni kulüp oluşturma işlemini sistem yöneticileriyle sınırlandırır
def create_new_club(club: ClubCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Verifies if the current user has the 'admin' role | Mevcut kullanıcının 'admin' rolüne sahip olup olmadığını doğrular
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Unauthorized action")
    return ClubRepository.create(db, club)

@router.get("/", response_model=list[ClubResponse]) # Public endpoint to list all available clubs | Tüm mevcut kulüpleri listelemek için herkese açık uç nokta
def get_clubs(db: Session = Depends(get_db)):
    return ClubRepository.get_all(db)