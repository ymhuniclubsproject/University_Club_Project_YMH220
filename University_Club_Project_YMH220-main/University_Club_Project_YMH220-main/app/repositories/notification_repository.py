from sqlalchemy.orm import Session
from app.models.notification import Notification

class NotificationRepository:
    @staticmethod
    def create(db: Session, user_id: int, message: str):
        db_obj = Notification(user_id=user_id, message=message)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj