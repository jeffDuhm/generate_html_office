from dotenv import load_dotenv
from fastapi import FastAPI
from corepy.shared.mysql.base import Base, engine
from api.user.router import router as router_user
from api.auth.router import router as router_auth
from api.site.router import router as router_site
from api.site.router import user_router as router_site_user

load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(title="Shazam API")
    Base.metadata.create_all(bind=engine)
    
    app.include_router(router_user, prefix="/users", tags=["users"])
    app.include_router(router_auth, prefix="/auth", tags=["auth"])
    app.include_router(router_site, prefix="/admin/sites", tags=["admin"])
    app.include_router(router_site_user, prefix="/sites", tags=["sites"])

    return app

app = create_app()