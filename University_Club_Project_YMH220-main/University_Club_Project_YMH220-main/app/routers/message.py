from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.club import Club
from app.repositories.message_repository import MessageRepository
from app.core.deps import get_db, get_current_user
from app.models.user import RoleEnum
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageResponse

router = APIRouter(prefix="/messages", tags=["Club Messaging"])

@router.post("/", response_model=MessageResponse)
def send_message(data: MessageCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role not in [RoleEnum.club_manager, RoleEnum.admin]:
        raise HTTPException(status_code=403, detail="Only club managers can send messages.")
    
    sender_club = db.query(Club).filter(Club.manager_id == current_user.id).first()
    if not sender_club:
        raise HTTPException(status_code=404, detail="Managed club not found.")

    db_msg = Message(sender_club_id=sender_club.id, **data.model_dump())
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg

@router.get("/conversation/{other_club_id}", response_model=List[MessageResponse])
def get_chat(other_club_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    my_club = db.query(Club).filter(Club.manager_id == current_user.id).first()
    if not my_club:
        raise HTTPException(status_code=404, detail="Club not found")
    return MessageRepository.get_conversation(db, my_club.id, other_club_id)