from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.club import Club
from app.schemas.club import ClubCreate

class ClubRepository: # Manages club database operations including creation and retrieval | Kulüp oluşturma ve getirme dahil veri tabanı işlemlerini yönetir
    @staticmethod
    def create(db: Session, club_data: ClubCreate): # Validates name uniqueness and saves a new club | İsim benzersizliğini doğrular ve yeni bir kulübü kaydeder
        existing_club = db.query(Club).filter(Club.name == club_data.name).first()
        if existing_club:
            raise HTTPException(status_code=400, detail="A club with this name already exists.")
            
        db_club = Club(**club_data.model_dump())
        db.add(db_club)
        db.commit()
        db.refresh(db_club)
        return db_club

    @staticmethod
    def get_all(db: Session): # Retrieves all registered clubs from the database | Veri tabanındaki tüm kayıtlı kulüpleri getirir
        return db.query(Club).all()

    @staticmethod
    def get_by_id(db: Session, club_id: int): # Finds a specific club by its unique ID | Benzersiz kimliği ile belirli bir kulübü bulur
        return db.query(Club).filter(Club.id == club_id).first()