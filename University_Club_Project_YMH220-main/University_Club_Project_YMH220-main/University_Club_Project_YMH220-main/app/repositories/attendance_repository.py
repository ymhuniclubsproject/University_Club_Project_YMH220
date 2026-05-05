from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceUpdate

class AttendanceRepository:
    @staticmethod
    def mark(db: Session, data: AttendanceUpdate):
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