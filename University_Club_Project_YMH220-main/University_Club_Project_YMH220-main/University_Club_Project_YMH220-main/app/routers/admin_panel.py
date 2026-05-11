from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.deps import get_db, get_current_user
from app.models.user import RoleEnum, User
from app.models.club import Club
from app.models.event import Event
from app.models.membership import Membership
from app.models.attendance import Attendance

router = APIRouter(prefix="/admin", tags=["Admin Panel"])

@router.get("/stats")
def get_system_stats(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Unauthorized action")
    return {
        "total_users": db.query(User).count(),
        "total_clubs": db.query(Club).count(),
        "total_events": db.query(Event).count()
    }

@router.get("/detailed-stats")
def get_detailed_stats(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Unauthorized action")

    most_active = db.query(Club.name, func.count(Event.id).label('count')).join(Event).group_by(Club.id).order_by(func.count(Event.id).desc()).first()
    most_members = db.query(Club.name, func.count(Membership.id).label('count')).join(Membership).group_by(Club.id).order_by(func.count(Membership.id).desc()).first()
    total_att = db.query(func.count(Attendance.id)).filter(Attendance.is_present == True).scalar()

    return {
        "most_active_club": most_active._asdict() if most_active else None,
        "most_members_club": most_members._asdict() if most_members else None,
        "total_attendance_count": total_att or 0
    }