from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceUpdate

class AttendanceRepository: # Manages attendance records by updating existing entries or creating new ones | Mevcut kayıtları güncelleyerek veya yeni oluşturarak katılım kayıtlarını yönetir
    @staticmethod
    def mark(db: Session, data: AttendanceUpdate): # Updates presence status for a user-event pair or adds a new record | Bir kullanıcı-etkinlik çifti için katılım durumunu günceller veya yeni kayıt ekler
        db_obj = db.query(Attendance).filter(
            Attendance.user_id == data.user_id, 
            Attendance.event_id == data.event_id
        ).first()
        
        if db_obj:
            db_obj.is_present = data.is_present
        else:
            db_obj = Attendance(**data.model_dump())
            db.add(db_obj)
            
        db.commit()
        db.refresh(db_obj)
        return db_obj