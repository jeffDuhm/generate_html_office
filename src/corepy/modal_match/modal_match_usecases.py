from sqlalchemy.orm import Session

from corepy.modal_match.modal_match_exceptions import (
    InvalidModalMatchUpdateError,
    ModalMatchConflictError,
    ModalMatchNotFoundError,
    SiteNotFoundError,
)
from corepy.modal_match.modal_match_messages import SuccessModalMatchMessages
from corepy.modal_match.modal_match_queries import ModalMatchQueries
from corepy.modal_match.modal_match_schemas import (
    CreateModalMatchSchema,
    ModalMatchSchema,
    UpdateModalMatchSchema,
)
from corepy.shared.schemas.response_schemas import ResponseSuccessSchema
from corepy.site.site_queries import SiteQueries

class ModalMatchUsecases:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_site(self, site_id: int, user_id: int) -> ResponseSuccessSchema:
        db_matches = ModalMatchQueries(self.db).get_all_by_site(
            user_id=user_id, site_id=site_id
        )

        matches = []
        for db_match in db_matches:
            match = ModalMatchSchema.model_validate(db_match)
            matches.append(match)

        return ResponseSuccessSchema(
            message=SuccessModalMatchMessages.MODAL_MATCH_LIST,
            data=matches,
        )

    def create(
        self, site_id: int, user_id: int, new_match: CreateModalMatchSchema
    ) -> ResponseSuccessSchema:
        db_site = SiteQueries(self.db).get_by_id(site_id)
        if not db_site or not db_site.is_active:
            raise SiteNotFoundError()

        queries = ModalMatchQueries(self.db)
        existing = queries.get_by_site_match(
            user_id=user_id, site_id=site_id, text=new_match.text
        )
        
        if existing is not None:
            return ResponseSuccessSchema(
                message=SuccessModalMatchMessages.MODAL_MATCH_EXISTS,
                data=ModalMatchSchema.model_validate(existing),
            )

        db_match = queries.create(
            user_id=user_id, site_id=site_id, text=new_match.text
        )

        return ResponseSuccessSchema(
            message=SuccessModalMatchMessages.MODAL_MATCH_CREATED,
            data=ModalMatchSchema.model_validate(db_match),
        )

    def update(
        self, match_id: int, user_id: int, match_update: UpdateModalMatchSchema
    ) -> ResponseSuccessSchema:
        queries = ModalMatchQueries(self.db)

        db_match = queries.get_by_id(match_id)
        if not db_match or db_match.user_id != user_id:
            raise ModalMatchNotFoundError()

        updates = match_update.model_dump(exclude_unset=True)
        if not updates:
            raise InvalidModalMatchUpdateError()

        for value in updates.values():
            if value is None:
                raise InvalidModalMatchUpdateError()

        existing = queries.get_by_site_match(
            user_id=user_id, site_id=db_match.site_id, text=updates["text"]
        )
        if existing is not None and existing.id != match_id:
            raise ModalMatchConflictError()

        match = queries.update(db_match, updates)

        return ResponseSuccessSchema(
            message=SuccessModalMatchMessages.MODAL_MATCH_UPDATED,
            data=ModalMatchSchema.model_validate(match),
        )

    def delete(self, match_id: int, user_id: int) -> ResponseSuccessSchema:
        queries = ModalMatchQueries(self.db)

        db_match = queries.get_by_id(match_id)
        if not db_match or db_match.user_id != user_id:
            raise ModalMatchNotFoundError()

        deleted = queries.delete(db_match)
        if not deleted:
            raise ModalMatchConflictError()

        return ResponseSuccessSchema(
            message=SuccessModalMatchMessages.MODAL_MATCH_DELETED
        )