from dotenv import load_dotenv
from fastapi import FastAPI
from corepy.shared.mysql.base import Base, engine
from api.user.router import router as router_user
from api.auth.router import router as router_auth
from api.site.router import router as router_site
from api.site.router import user_router as router_site_user
from api.widget.router import router as router_widget
from api.widget_match.router import router as router_widget_match
from api.modal_match.router import router as router_modal_match
from api.url_replacement.router import router as router_url_replacement
from api.conversion_log.router import router as router_conversion_log
from api.site_config.router import router as router_site_config
from api.conversion.router import router as router_conversion

load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(title="Shazam API")
    Base.metadata.create_all(bind=engine)
    
    app.include_router(router_user, prefix="/users", tags=["users"])
    app.include_router(router_auth, prefix="/auth", tags=["auth"])
    app.include_router(router_site, prefix="/admin/sites", tags=["admin"])
    app.include_router(router_site_user, prefix="/sites", tags=["sites"])
    app.include_router(router_widget, prefix="/admin/sites/{site_id}/widgets", tags=["admin"])
    app.include_router(router_widget_match, tags=["widget-matches"])
    app.include_router(router_modal_match, tags=["modal-matches"])
    app.include_router(router_url_replacement, tags=["url-replacements"])
    app.include_router(router_conversion_log, prefix="/admin/conversion-logs", tags=["admin"])
    app.include_router(router_site_config, tags=["site-config"])
    app.include_router(router_conversion, tags=["conversion"])

    return app

app = create_app()