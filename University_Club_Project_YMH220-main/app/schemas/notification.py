from pydantic import BaseModel
from datetime import datetime

class NotificationResponse(BaseModel): # Schema for returning notification details to the user | Bildirim detaylarını kullanıcıya döndürmek için kullanılan şema
    id: int
    message: str
    is_read: bool
    created_at: datetime
    class Config:
        from_attributes = True # Enables mapping from database model attributes | Veri tabanı model özelliklerinden eşlemeyi sağlar