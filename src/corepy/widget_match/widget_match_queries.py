from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from corepy.widget_match.widget_match_dbs import WidgetMatchesDB
from corepy.widget.widget_dbs import WidgetsDB
    
class WidgetMatchQueries:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, match_id: int) -> Optional[WidgetMatchesDB]:
        query = select(WidgetMatchesDB).where(WidgetMatchesDB.id == match_id)
        db_match = self.db.scalars(query).first()
        return db_match

    def get_all_by_widget(self, widget_id: int, user_id: int) -> list[WidgetMatchesDB]:
        query = (
            select(WidgetMatchesDB)
            .where(
                WidgetMatchesDB.widget_id == widget_id,
                WidgetMatchesDB.user_id == user_id,
            )
            .order_by(WidgetMatchesDB.id)
        )
        db_matches = self.db.scalars(query).all()
        return db_matches

    def get_all_by_site(self, site_id: int, user_id: int) -> list[WidgetMatchesDB]:
        query = (
            select(WidgetMatchesDB)
            .join(WidgetsDB, WidgetMatchesDB.widget_id == WidgetsDB.id)
            .where(
                WidgetsDB.site_id == site_id,
                WidgetMatchesDB.user_id == user_id,
            )
            .order_by(WidgetMatchesDB.id)
        )
        db_matches = self.db.scalars(query).all()
        return db_matches

    def get_by_site_match(self, site_id: int, user_id: int, text: str) -> Optional[WidgetMatchesDB]:
        query = (
            select(WidgetMatchesDB)
            .join(WidgetsDB, WidgetMatchesDB.widget_id == WidgetsDB.id)
            .where(
                WidgetsDB.site_id == site_id,
                WidgetMatchesDB.user_id == user_id,
                WidgetMatchesDB.text == text,                   
            )
        )
        db_match = self.db.scalars(query).first()
        return db_match

    def create(self, widget_id: int, user_id: int, text: str) -> WidgetMatchesDB:
        db_match = WidgetMatchesDB(
            widget_id=widget_id,
            user_id=user_id,
            text=text,
        )
        self.db.add(db_match)
        self.db.commit()
        self.db.refresh(db_match)
        return db_match

    def update(self, db_match: WidgetMatchesDB, updates: dict) -> WidgetMatchesDB:
        for key, value in updates.items():
            setattr(db_match, key, value)

        self.db.commit()
        self.db.refresh(db_match)
        return db_match

    def delete(self, db_match: WidgetMatchesDB) -> bool:
        try:
            self.db.delete(db_match)
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False