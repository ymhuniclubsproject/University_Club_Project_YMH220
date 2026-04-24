from sqlalchemy.orm import Session
from app.models.rating import Rating
from app.schemas.rating import RatingCreate

class RatingRepository:
    @staticmethod
    def create(db: Session, user_id: int, data: RatingCreate):
        db_rating = Rating(**data.model_dump(), user_id=user_id)
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating