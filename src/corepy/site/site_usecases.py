from sqlalchemy.orm import Session

from corepy.shared.logging.logging import Logger
from corepy.shared.schemas.response_schemas import ResponseSuccessSchema
from corepy.site.site_queries import SiteQueries
from corepy.site.site_schemas import (
    CreateSiteSchema,
    UpdateSiteSchema,
    SiteSchema
)
from corepy.site.site_messages import SuccessSiteMessages
from corepy.site.site_exceptions import (
    SiteNotFoundError,
    SiteNameAlreadyExistsError,
    SiteHasRelatedRecordsError,
    SiteInvalidUpdateError
)

class SiteUsecases:
    def __init__(self, db: Session):
        self.db = db
        self.logger = Logger(__name__)
        
    def get_all(self) -> ResponseSuccessSchema:
        db_sites = SiteQueries(self.db).get_all()
        
        sites = []
        for db_site in db_sites:
            sites.append(SiteSchema.model_validate(db_site))
            
        return ResponseSuccessSchema(message=SuccessSiteMessages.SITES_LIST, data=sites)
    
    def get_all_active(self) -> ResponseSuccessSchema:
        db_sites = SiteQueries(self.db).get_all_active()
        
        sites_active = []
        for db_site in db_sites:
            sites_active.append(SiteSchema.model_validate(db_site))
        
        return ResponseSuccessSchema(message=SuccessSiteMessages.SITES_LIST, data=sites_active)

    def get_by_id(self, site_id: int) -> ResponseSuccessSchema:
        db_site = SiteQueries(self.db).get_by_id(site_id)
        if not db_site:
            raise SiteNotFoundError()

        site = SiteSchema.model_validate(db_site)
        return ResponseSuccessSchema(message=SuccessSiteMessages.SITE_GET, data=site)
    
    def create(self, new_site: CreateSiteSchema) -> ResponseSuccessSchema:
        queries = SiteQueries(self.db)
        
        if queries.get_by_name(new_site.name):
            raise SiteNameAlreadyExistsError()
        
        db_site = queries.create(name=new_site.name)
        
        site = SiteSchema.model_validate(db_site)
        return ResponseSuccessSchema(message=SuccessSiteMessages.SITE_CREATED, data=site)
    
    def update(self, site_id: int, site_update: UpdateSiteSchema) -> ResponseSuccessSchema:
        queries = SiteQueries(self.db)
        
        db_site = queries.get_by_id(site_id)
        if not db_site:
            raise SiteNotFoundError()
        
        updates = site_update.model_dump(exclude_unset=True)
        
        if not updates:
            raise SiteInvalidUpdateError()
        
        for value in updates.values():
            if value is None:
                raise SiteInvalidUpdateError()
        
        new_name = updates.get("name")
        if new_name is not None: 
            existing_site = queries.get_by_name(new_name)
            if existing_site is not None and existing_site.id != site_id:
                raise SiteNameAlreadyExistsError()
        db_site = queries.update(db_site, updates)
        self.logger.info(f"Site updated: id={db_site.id}")
        
        site = SiteSchema.model_validate(db_site)
        
        return ResponseSuccessSchema(message=SuccessSiteMessages.SITE_UPDATED, data=site)
        
    def delete(self, site_id: int) -> ResponseSuccessSchema:
        queries = SiteQueries(self.db)
        
        db_site = queries.get_by_id(site_id)
        if not db_site:
            raise SiteNotFoundError()
        
        deleted = queries.delete(db_site)
        if not deleted:
            raise SiteHasRelatedRecordsError()

        self.logger.info(f"Site deleted: id={site_id}")
        
        return ResponseSuccessSchema(message=SuccessSiteMessages.SITE_DELETED)
        
        