from sqlalchemy.orm import Session
from app.models.rating import Rating
from app.schemas.rating import RatingCreate

class RatingRepository: # Handles the storage and persistence of event ratings and feedback | Etkinlik puanlamalarının ve geri bildirimlerin kaydedilmesini yönetir
    @staticmethod
    def create(db: Session, user_id: int, data: RatingCreate): # Saves a new rating record linked to a specific user and event | Belirli bir kullanıcı ve etkinlikle bağlantılı yeni bir puanlama kaydeder
        db_rating = Rating(**data.model_dump(), user_id=user_id)
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating