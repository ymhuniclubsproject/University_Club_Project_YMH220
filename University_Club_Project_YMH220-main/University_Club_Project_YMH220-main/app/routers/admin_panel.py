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

@router.get("/stats") # Provides high-level system overview for administrators | Yöneticiler için üst düzey sistem özeti sağlar
def get_system_stats(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Unauthorized action")
    return {
        "total_users": db.query(User).count(),
        "total_clubs": db.query(Club).count(),
        "total_events": db.query(Event).count()
    }

@router.get("/detailed-stats") # Aggregates club activities, membership counts, and attendance metrics | Kulüp aktivitelerini, üye sayılarını ve katılım metriklerini birleştirir
def get_detailed_stats(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Unauthorized action")

    # Identifies the club with the highest number of organized events | En fazla etkinlik düzenleyen kulübü belirler
    most_active = db.query(Club.name, func.count(Event.id).label('count')).join(Event).group_by(Club.id).order_by(func.count(Event.id).desc()).first()
    
    # Identifies the club with the largest membership base | En büyük üye tabanına sahip kulübü belirler
    most_members = db.query(Club.name, func.count(Membership.id).label('count')).join(Membership).group_by(Club.id).order_by(func.count(Membership.id).desc()).first()
    
    # Calculates the total number of confirmed event attendances | Onaylanmış toplam etkinlik katılım sayısını hesaplar
    total_att = db.query(func.count(Attendance.id)).filter(Attendance.is_present == True).scalar()

    return {
        "most_active_club": most_active._asdict() if most_active else None,
        "most_members_club": most_members._asdict() if most_members else None,
        "total_attendance_count": total_att or 0
    }