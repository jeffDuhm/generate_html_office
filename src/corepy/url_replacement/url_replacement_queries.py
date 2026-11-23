from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from corepy.url_replacement.url_replacement_dbs import UrlReplacementsDB

class UrlReplacementQueries:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, url_replacement_id: int) -> Optional[UrlReplacementsDB]:
        query = select(UrlReplacementsDB).where(UrlReplacementsDB.id == url_replacement_id)
        db_url_replacement = self.db.scalars(query).first()
        return db_url_replacement
    
    def get_by_source_url(self, user_id: int, site_id: int, source_url: str) -> Optional[UrlReplacementsDB]:
        query = (
            select(UrlReplacementsDB)
            .where(
                UrlReplacementsDB.user_id == user_id,
                UrlReplacementsDB.site_id == site_id,
                UrlReplacementsDB.source_url == source_url,
            )
        )
        db_url_replacement = self.db.scalars(query).first()
        return db_url_replacement
    
    def get_all_by_site(self, user_id: int, site_id: int) -> list[UrlReplacementsDB]:
        query = (
            select(UrlReplacementsDB)
            .where(
                UrlReplacementsDB.user_id == user_id,
                UrlReplacementsDB.site_id == site_id,
            )
            .order_by(UrlReplacementsDB.id)
        )
        db_url_replacements = self.db.scalars(query).all()
        return db_url_replacements
    
    def create(self, user_id: int, site_id: int, source_url: str, target_url: str) -> UrlReplacementsDB:
        db_url_replacement = UrlReplacementsDB(
            user_id=user_id,
            site_id=site_id,
            source_url=source_url,
            target_url=target_url,
        )
        self.db.add(db_url_replacement)
        self.db.commit()
        self.db.refresh(db_url_replacement)
        return db_url_replacement
    
    def update(self, db_url_replacement: UrlReplacementsDB, updates: dict) -> UrlReplacementsDB:
        
        for key, value in updates.items():
            setattr(db_url_replacement, key, value)
            
        self.db.commit()
        self.db.refresh(db_url_replacement)
        return db_url_replacement
    
    def delete(self, db_url_replacement: UrlReplacementsDB) -> bool:
        try:
            self.db.delete(db_url_replacement)
            self.db.commit()
            return True
        
        except IntegrityError:
            self.db.rollback()
            return False