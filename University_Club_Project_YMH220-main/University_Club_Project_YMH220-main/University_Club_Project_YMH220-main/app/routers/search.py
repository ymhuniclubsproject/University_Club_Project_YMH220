from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
import logging

from app.core.deps import get_db
from app.services.auth_service import get_current_user
from app.models.club import Club
from app.schemas.club import ClubResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/search", tags=["Search & Profile"])


@router.get("/clubs", response_model=List[ClubResponse])
def search_clubs(
    category: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Club)
        if category:
            query = query.filter(Club.category == category)
        if q:
            query = query.filter(
                Club.name.contains(q) | Club.description.contains(q)
            )
        return query.all()
    except SQLAlchemyError as e:
        logger.error(f"Database error during club search: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred.")
    except Exception as e:
        logger.error(f"Unexpected error during club search: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@router.get("/profile/{club_id}", response_model=ClubResponse)
def get_club_profile(club_id: int, db: Session = Depends(get_db)):
    try:
        club = db.query(Club).filter(Club.id == club_id).first()
        if not club:
            raise HTTPException(status_code=404, detail="Club not found")
        return club
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching club {club_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred.")
    except Exception as e:
        logger.error(f"Unexpected error while fetching club {club_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@router.post("/favorite/{club_id}")
def add_favorite(
    club_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        club = db.query(Club).filter(Club.id == club_id).first()
        if not club:
            raise HTTPException(status_code=404, detail="Club not found")
        if club not in current_user.favorites:
            current_user.favorites.append(club)
            db.commit()
        return {"message": "Added to favorites"}
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error while adding favorite {club_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred.")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while adding favorite {club_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@router.get("/my-favorites", response_model=List[ClubResponse])
def get_favorites(current_user=Depends(get_current_user)):
    try:
        return current_user.favorites
    except Exception as e:
        logger.error(f"Unexpected error while fetching favorites: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")