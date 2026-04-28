from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import RoleEnum
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceUpdate, AttendanceResponse

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post("/", response_model=AttendanceResponse)
def mark_attendance(data: AttendanceUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role not in [RoleEnum.club_manager, RoleEnum.admin]:
        raise HTTPException(status_code=403, detail="Unauthorized action")
    
    db_obj = db.query(Attendance).filter(Attendance.user_id == data.user_id, Attendance.event_id == data.event_id).first()
    if db_obj:
        db_obj.is_present = data.is_present
    else:
        db_obj = Attendance(**data.model_dump())
        db.add(db_obj)
    
    db.commit()
    db.refresh(db_obj)
    return db_obj