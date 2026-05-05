from pydantic import BaseModel

class AttendanceUpdate(BaseModel): # Schema for updating or recording a user's attendance status | Bir kullanıcının katılım durumunu güncellemek veya kaydetmek için şema
    user_id: int
    event_id: int
    is_present: bool

class AttendanceResponse(AttendanceUpdate): # Schema for returning attendance data with its database ID | Katılım verilerini veri tabanı kimliği ile birlikte döndürmek için şema
    id: int
    class Config:
        from_attributes = True # Allows Pydantic to read data from ORM objects | Pydantic'in ORM nesnelerinden veri okumasına izin verir