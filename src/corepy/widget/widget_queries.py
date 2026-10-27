from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from corepy.widget.widget_dbs import WidgetsDB

class WidgetQueries:
    
    def __init__(self, db: Session):
        self.db = db
        
    def get_all_by_site(self, site_id: int) -> list[WidgetsDB]:
        query = select(WidgetsDB).where(WidgetsDB.site_id == site_id)
        db_widgets = self.db.scalars(query).all()
        return db_widgets

    def get_by_id(self, widget_id: int) -> Optional[WidgetsDB]:
        query = select(WidgetsDB).where(WidgetsDB.id == widget_id)
        db_widget = self.db.scalars(query).first()
        return db_widget
    
    def get_by_shortcode(self, site_id: int, shortcode: str) -> Optional[WidgetsDB]:
        query = select(WidgetsDB).where(WidgetsDB.site_id == site_id).where(WidgetsDB.shortcode == shortcode)
        db_widget = self.db.scalars(query).first()
        return db_widget
    
    def create(self, site_id: int, shortcode: str) -> WidgetsDB:
        
        db_widget = WidgetsDB(
            site_id=site_id,
            shortcode=shortcode
        )
        
        self.db.add(db_widget)
        self.db.commit()
        self.db.refresh(db_widget)
        return db_widget
    
    def update(self, db_widget: WidgetsDB, updates: dict) -> WidgetsDB:
        for key, value in updates.items():
            setattr(db_widget, key, value)
            
        self.db.commit()
        self.db.refresh(db_widget)
        return db_widget
    
    def delete(self, db_widget: WidgetsDB) -> bool:
        try:
            self.db.delete(db_widget)
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False