from sqlalchemy.orm import Session
from app.models.membership import Membership

class MembershipRepository:
    @staticmethod
    def create_request(db: Session, user_id: int, club_id: int):
        db_membership = Membership(user_id=user_id, club_id=club_id, status="pending")
        db.add(db_membership)
        db.commit()
        db.refresh(db_membership)
        return db_membership

    @staticmethod
    def update_status(db: Session, membership_id: int, status: str):
        db_membership = db.query(Membership).filter(Membership.id == membership_id).first()
        if db_membership:
            db_membership.status = status
            db.commit()
            db.refresh(db_membership)
        return db_membership