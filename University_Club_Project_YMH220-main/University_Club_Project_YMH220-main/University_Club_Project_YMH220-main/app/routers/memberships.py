from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import RoleEnum
from app.repositories.membership_repository import MembershipRepository
from app.schemas.membership import MembershipUpdate, MembershipResponse

router = APIRouter(prefix="/memberships", tags=["Memberships"])

@router.post("/join/{club_id}", response_model=MembershipResponse)
def request_join(club_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return MembershipRepository.create_request(db, current_user.id, club_id)

@router.put("/approve/{membership_id}", response_model=MembershipResponse)
def approve_member(
    membership_id: int, 
    data: MembershipUpdate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    if current_user.role not in [RoleEnum.club_manager, RoleEnum.admin]:
        raise HTTPException(status_code=403, detail="You do not have permission to approve.")
    return MembershipRepository.update_status(db, membership_id, data.status)