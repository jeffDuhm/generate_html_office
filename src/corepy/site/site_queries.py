from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from corepy.site.site_dbs import SitesDB

class SiteQueries:
    
    def __init__(self, db: Session):
        self.db = db
        
    def get_all(self) -> list[SitesDB]:
        query = select(SitesDB).order_by(SitesDB.name)
        db_sites = self.db.scalars(query).all()
        return db_sites
    
    def get_all_active(self) -> list[SitesDB]:
        query = select(SitesDB).where(SitesDB.is_active.is_(True)).order_by(SitesDB.name)
        db_sites = self.db.scalars(query).all()
        return db_sites
    
    def get_by_id(self, site_id: int) -> Optional[SitesDB]:
        query = select(SitesDB).where(site_id == SitesDB.id)
        db_site = self.db.scalars(query).first()
        return db_site
    
    def get_by_name(self, name: str) -> Optional[SitesDB]:
        query = select(SitesDB).where(SitesDB.name == name)
        db_site = self.db.scalars(query).first()
        return db_site
    
    def create(self, name: str) -> SitesDB:
        db_site = SitesDB(
            name=name
        )
        self.db.add(db_site)
        self.db.commit()
        self.db.refresh(db_site)
        return db_site
    
    def update(self, db_site: SitesDB, updates: dict) -> SitesDB:
        for key, value in updates.items():
            setattr(db_site, key, value)
            
        self.db.commit()
        self.db.refresh(db_site)
        return db_site

    def delete(self, db_site: SitesDB) -> bool:
        try:
            self.db.delete(db_site)
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False
            