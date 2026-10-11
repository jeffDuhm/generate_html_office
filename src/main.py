from dotenv import load_dotenv
from fastapi import FastAPI
from corepy.shared.mysql.base import Base, engine
from api.user.router import router as router_user

load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(title="Shazam API")
    Base.metadata.create_all(bind=engine)
    
    app.include_router(router_user, prefix="/users", tags=["users"])

    return app

app = create_app()