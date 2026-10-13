from dotenv import load_dotenv
from fastapi import FastAPI
from corepy.shared.mysql.base import Base, engine
from api.user.router import router as router_user
from api.auth.router import router as router_auth
from corepy.user.user_usecases import UserUsecases

load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(title="Shazam API")
    Base.metadata.create_all(bind=engine)
    UserUsecases().ensure_first_admin()
    
    app.include_router(router_user, prefix="/users", tags=["users"])
    app.include_router(router_auth, prefix="/auth", tags=["auth"])

    return app

app = create_app()