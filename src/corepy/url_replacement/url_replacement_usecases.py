from sqlalchemy.orm import Session

from corepy.shared.logging.logging import Logger
from corepy.shared.schemas.response_schemas import ResponseSuccessSchema
from corepy.site.site_exceptions import SiteNotFoundError
from corepy.site.site_queries import SiteQueries
from corepy.url_replacement.url_replacement_exceptions import (
    InvalidUrlReplacementUpdateError,
    UrlReplacementAlreadyExistsError,
    UrlReplacementNotFoundError,
    UrlReplacementDeleteError
)
from corepy.url_replacement.url_replacement_messages import (
    SuccessUrlReplacementMessages,
)
from corepy.url_replacement.url_replacement_queries import UrlReplacementQueries
from corepy.url_replacement.url_replacement_schemas import (
    CreateUrlReplacementSchema,
    UpdateUrlReplacementSchema,
    UrlReplacementSchema,
)

class UrlReplacementUsecases:

    def __init__(self, db: Session):
        self.db = db
        
    def get_all_by_site(self, user_id: int, site_id: int) -> ResponseSuccessSchema:
        
        db_site = SiteQueries(self.db).get_by_id(site_id)
        if not db_site or not db_site.is_active:
            raise SiteNotFoundError()
        
        queries = UrlReplacementQueries(self.db)
        db_url_replacements = queries.get_all_by_site(
            user_id=user_id,
            site_id=site_id,
        )
        
        url_replacements = []
        for db_url_replacement in db_url_replacements:
            url_replacement = UrlReplacementSchema.model_validate(db_url_replacement)
            url_replacements.append(url_replacement)

        return ResponseSuccessSchema(
            message=SuccessUrlReplacementMessages.URL_REPLACEMENTS_LIST,
            data=url_replacements,
        )

    def create(
        self, user_id: int, site_id: int, new_replacement: CreateUrlReplacementSchema
    ) -> ResponseSuccessSchema:
        db_site = SiteQueries(self.db).get_by_id(site_id)
        if not db_site or not db_site.is_active:
            raise SiteNotFoundError()

        queries = UrlReplacementQueries(self.db)
        existing = queries.get_by_source_url(
            user_id=user_id,
            site_id=site_id,
            source_url=new_replacement.source_url,
        )

        if existing is not None:
            if existing.target_url == new_replacement.target_url:
                url_replacement = UrlReplacementSchema.model_validate(existing)
                return ResponseSuccessSchema(
                    message=SuccessUrlReplacementMessages.URL_REPLACEMENT_EXISTS,
                    data=url_replacement,
                )
            raise UrlReplacementAlreadyExistsError()

        db_url_replacement = queries.create(
            user_id=user_id,
            site_id=site_id,
            source_url=new_replacement.source_url,
            target_url=new_replacement.target_url,
        )

        url_replacement = UrlReplacementSchema.model_validate(db_url_replacement)
        
        return ResponseSuccessSchema(
            message=SuccessUrlReplacementMessages.URL_REPLACEMENT_CREATED,
            data=url_replacement,
        )

    def update(
        self,
        user_id: int,
        url_replacement_id: int,
        url_replacement_update: UpdateUrlReplacementSchema,
    ) -> ResponseSuccessSchema:
        
        queries = UrlReplacementQueries(self.db)
        
        db_url_replacement = queries.get_by_id(url_replacement_id)

        if not db_url_replacement or db_url_replacement.user_id != user_id:
            raise UrlReplacementNotFoundError()

        updates = url_replacement_update.model_dump(exclude_unset=True)

        if not updates:
            raise InvalidUrlReplacementUpdateError()

        for value in updates.values():
            if value is None:
                raise InvalidUrlReplacementUpdateError()

        new_source_url = updates.get("source_url")

        if new_source_url is not None and new_source_url != db_url_replacement.source_url:
            existing = queries.get_by_source_url(
                user_id=user_id,
                site_id=db_url_replacement.site_id,
                source_url=new_source_url,
            )
            if existing is not None and existing.id != url_replacement_id:
                raise UrlReplacementAlreadyExistsError()

        db_url_replacement = queries.update(db_url_replacement, updates)

        url_replacement = UrlReplacementSchema.model_validate(db_url_replacement)
        return ResponseSuccessSchema(
            message=SuccessUrlReplacementMessages.URL_REPLACEMENT_UPDATED,
            data=url_replacement,
        )

    def delete(self, user_id: int, url_replacement_id: int) -> ResponseSuccessSchema:
        
        queries = UrlReplacementQueries(self.db)
        
        db_url_replacement = queries.get_by_id(url_replacement_id)
        
        if not db_url_replacement or db_url_replacement.user_id != user_id:
            raise UrlReplacementNotFoundError()

        deleted = queries.delete(db_url_replacement)
        
        if not deleted:
            raise UrlReplacementDeleteError()

        return ResponseSuccessSchema(
            message=SuccessUrlReplacementMessages.URL_REPLACEMENT_DELETED
        )