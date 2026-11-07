from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from corepy.user.user_dbs import UsersDB


class UserQueries:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[UsersDB]:
        query = select(UsersDB).order_by(UsersDB.id)
        db_users = self.db.scalars(query).all()
        return db_users

    def get_by_id(self, user_id: int) -> Optional[UsersDB]:
        query = select(UsersDB).where(UsersDB.id == user_id)
        db_user = self.db.scalars(query).first()
        return db_user

    def get_by_email(self, email: str) -> Optional[UsersDB]:
        query = select(UsersDB).where(UsersDB.email == email.lower())
        db_user = self.db.scalars(query).first()
        return db_user
    
    def exists_admin(self) -> bool:
        # Verifica si existe un admin activo
        query = select(UsersDB.id).where(
            UsersDB.is_admin.is_(True),
            UsersDB.is_active.is_(True),
        )
        db_user = self.db.scalars(query).first()
        return db_user is not None

    def create(
        self, email: str, name: str, password_hash: str, is_admin: bool = False
    ) -> UsersDB:
        db_user = UsersDB(
            email=email.lower(),
            name=name,
            password=password_hash,
            is_admin=is_admin,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, db_user: UsersDB, updates: dict) -> UsersDB:
        
        for key, value in updates.items():
            setattr(db_user, key, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete(self, db_user: UsersDB) -> bool:
        try:
            self.db.delete(db_user)
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False