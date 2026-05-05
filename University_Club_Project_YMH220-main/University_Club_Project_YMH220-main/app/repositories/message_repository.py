from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.message import Message
from app.schemas.message import MessageCreate

class MessageRepository: # Manages messaging logic and conversation history between clubs | Kulüpler arası mesajlaşma mantığını ve konuşma geçmişini yönetir
    @staticmethod
    def send(db: Session, sender_id: int, data: MessageCreate): # Persists a new message between two clubs to the database | İki kulüp arasındaki yeni bir mesajı veri tabanına kaydeder
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
    def get_club_messages(db: Session, club_id: int): # Retrieves all sent and received messages for a specific club | Belirli bir kulübün gönderdiği ve aldığı tüm mesajları getirir
        return db.query(Message).filter(
            or_(
                Message.sender_club_id == club_id,
                Message.receiver_club_id == club_id
            )
        ).all()

    @staticmethod
    def get_conversation(db: Session, club_a: int, club_b: int): # Fetches chronological chat history between two specific clubs | İki belirli kulüp arasındaki kronolojik sohbet geçmişini çeker
        return db.query(Message).filter(
            or_(
                (Message.sender_club_id == club_a) & (Message.receiver_club_id == club_b),
                (Message.sender_club_id == club_b) & (Message.receiver_club_id == club_a)
            )
        ).order_by(Message.timestamp.asc()).all()