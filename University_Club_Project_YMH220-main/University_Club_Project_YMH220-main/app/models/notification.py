from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from datetime import datetime
from app.models.base import Base

class Notification(Base): # Stores system notifications for users and their read status | Kullanıcılar için sistem bildirimlerini ve okunma durumlarını tutar
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id")) # Links the notification to a specific recipient | Bildirimi belirli bir alıcıya bağlar
    message = Column(String)
    is_read = Column(Boolean, default=False) # Tracks whether the user has seen the notification | Kullanıcının bildirimi görüp görmediğini takip eder
    created_at = Column(DateTime, default=datetime.utcnow) # Automatically stamps the notification creation time | Bildirim oluşturulma zamanını otomatik olarak damgalar