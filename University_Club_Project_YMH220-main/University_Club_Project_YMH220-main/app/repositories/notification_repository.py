from sqlalchemy.orm import Session
from app.models.notification import Notification

class NotificationRepository: # Manages system notifications by persisting messages for specific users | Belirli kullanıcılar için mesajları kaydederek sistem bildirimlerini yönetir
    @staticmethod
    def create(db: Session, user_id: int, message: str): # Creates and saves a new notification record to the database | Veri tabanına yeni bir bildirim kaydı oluşturur ve kaydeder
        db_obj = Notification(user_id=user_id, message=message)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj