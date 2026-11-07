import os

from sqlalchemy.orm import Session

from corepy.shared.logging.logging import Logger
from corepy.shared.schemas.response_schemas import ResponseSuccessSchema
from corepy.shared.utils.password import Password
from corepy.user.user_exceptions import (
    CannotDeleteSelfError,
    InvalidCredentialsError,
    RepeatedEmailError,
    UserInUseError,
    UserNotFoundError,
    UserInvalidUpdateError
)
from corepy.user.user_messages import SuccessUserMessages
from corepy.user.user_queries import UserQueries
from corepy.user.user_schemas import (
    CreateUserSchema,
    UpdateUserSchema,
    UserAuthSchema,
    UserSchema,
)

class UserUsecases:
    def __init__(self, db: Session):
        self.db = db
        self.logger = Logger(__name__)

    def get_all(self) -> ResponseSuccessSchema:
        db_users = UserQueries(self.db).get_all()

        users = []
        for db_user in db_users:
            users.append(UserSchema.model_validate(db_user))

        return ResponseSuccessSchema(message=SuccessUserMessages.USER_LIST, data=users)

    def get_by_id(self, user_id: int) -> ResponseSuccessSchema:
        db_user = UserQueries(self.db).get_by_id(user_id)
        if not db_user:
            raise UserNotFoundError()

        user = UserSchema.model_validate(db_user)
        return ResponseSuccessSchema(message=SuccessUserMessages.USER_GET, data=user)

    def create(self, new_user: CreateUserSchema) -> ResponseSuccessSchema:
        queries = UserQueries(self.db)

        if queries.get_by_email(new_user.email):
            raise RepeatedEmailError()

        password_hash = Password.generate(new_user.password)
        db_user = queries.create(
            email=new_user.email,
            name=new_user.name,
            password_hash=password_hash,
            is_admin=new_user.is_admin,
        )

        user = UserSchema.model_validate(db_user)
        return ResponseSuccessSchema(message=SuccessUserMessages.USER_CREATED, data=user)

    def update(self, user_id: int, user_update: UpdateUserSchema) -> ResponseSuccessSchema:
        queries = UserQueries(self.db)

        db_user = queries.get_by_id(user_id)
        if not db_user:
            raise UserNotFoundError()

        updates = user_update.model_dump(exclude_unset=True)
        
        if not updates:
            raise UserInvalidUpdateError()

        if "email" in updates:
            other_user = queries.get_by_email(updates["email"])
            if other_user is not None and other_user.id != user_id:
                raise RepeatedEmailError()

        if "password" in updates:
            updates["password"] = Password.generate(updates["password"])

        db_user = queries.update(db_user, updates)

        user = UserSchema.model_validate(db_user)
        return ResponseSuccessSchema(message=SuccessUserMessages.USER_UPDATED, data=user)

    def authenticate(self, credentials: UserAuthSchema):

        db_user = UserQueries(self.db).get_by_email(credentials.email)
        if not db_user:
            raise InvalidCredentialsError()

        if not Password.verify(credentials.password, db_user.password):
            raise InvalidCredentialsError()

        if not db_user.is_active:
            raise InvalidCredentialsError()

        return db_user
        
    def delete(self, user_id: int, current_user_id: int) -> ResponseSuccessSchema:
        if user_id == current_user_id:
            raise CannotDeleteSelfError()
        
        queries = UserQueries(self.db)
        db_user = queries.get_by_id(user_id)
        if not db_user:
            raise UserNotFoundError()
        
        deleted = queries.delete(db_user)
        if not deleted:
            raise UserInUseError()
        
        return ResponseSuccessSchema(message=SuccessUserMessages.USER_DELETED)