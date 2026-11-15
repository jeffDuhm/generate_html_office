from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from corepy.modal_match.modal_match_dbs import ModalMatchesDB

class ModalMatchQueries:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, match_id: int) -> Optional[ModalMatchesDB]:
        query = select(ModalMatchesDB).where(ModalMatchesDB.id == match_id)
        db_match = self.db.scalars(query).first()
        return db_match
    
    def get_all_by_site(self, user_id: int, site_id: int) -> list[ModalMatchesDB]:
        query = (
            select(ModalMatchesDB)
            .where(
                ModalMatchesDB.user_id == user_id,
                ModalMatchesDB.site_id == site_id,
            )
            .order_by(ModalMatchesDB.id)
        )
        db_matches = self.db.scalars(query).all()
        return db_matches
    
    def get_by_site_match(self, user_id: int, site_id: int, text: str) -> Optional[ModalMatchesDB]:
        query = (
            select(ModalMatchesDB)
            .where(
                ModalMatchesDB.user_id == user_id,
                ModalMatchesDB.site_id == site_id,
                ModalMatchesDB.text == text,
            )
        )
        db_match = self.db.scalars(query).first()
        return db_match
    
    def create(self, user_id: int, site_id: int, text: str) -> ModalMatchesDB:
        db_match = ModalMatchesDB(
            user_id=user_id,
            site_id=site_id,
            text=text,
        )
        self.db.add(db_match)
        self.db.commit()
        self.db.refresh(db_match)
        return db_match
    
    def update(self, db_match: ModalMatchesDB, updates: dict) -> ModalMatchesDB:
        
        for key, value in updates.items():
            setattr(db_match, key, value)
        
        self.db.commit()
        self.db.refresh(db_match)
        return db_match

    def delete(self, db_match: ModalMatchesDB) -> bool:
        try:
            self.db.delete(db_match)
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False
            