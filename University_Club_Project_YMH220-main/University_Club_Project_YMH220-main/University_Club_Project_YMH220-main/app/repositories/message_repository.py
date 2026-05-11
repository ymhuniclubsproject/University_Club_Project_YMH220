from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.message import Message
from app.schemas.message import MessageCreate

class MessageRepository:
    @staticmethod
    def send(db: Session, sender_id: int, data: MessageCreate):
        db_obj = Message(
            sender_club_id=sender_id,
            receiver_club_id=data.receiver_club_id,
            content=data.content
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def get_club_messages(db: Session, club_id: int):
        return db.query(Message).filter(
            or_(
                Message.sender_club_id == club_id,
                Message.receiver_club_id == club_id
            )
        ).all()

    @staticmethod
    def get_conversation(db: Session, club_a: int, club_b: int):
        return db.query(Message).filter(
            or_(
                (Message.sender_club_id == club_a) & (Message.receiver_club_id == club_b),
                (Message.sender_club_id == club_b) & (Message.receiver_club_id == club_a)
            )
        ).order_by(Message.timestamp.asc()).all()