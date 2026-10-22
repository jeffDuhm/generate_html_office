import os

from dotenv import load_dotenv

from corepy.shared.mysql.base import SessionLocal, Base, engine
from corepy.shared.utils.password import Password
from corepy.user.user_queries import UserQueries
from corepy.shared.logging.logging import Logger

load_dotenv()

logger = Logger(__name__)

def create_first_admin():
    
    db = SessionLocal()
    
    try: 
        queries = UserQueries(db)
        if queries.exists_admin():
            return 
        
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")
        
        if not admin_email or not admin_password:
            logger.warning("No admin exists and ADMIN_EMAIL/ADMIN_PASSWORD are not set")
        
        existing_user = queries.get_by_email(admin_email)
        
        if existing_user:
            queries.update(existing_user, {"is_admin": True, "is_active": True})
            logger.info("Existing user promoted to admin")
            return
        
        queries.create(
            email=admin_email,
            name="Admin",
            password_hash=Password.generate(admin_password),
            is_admin=True
        )
        logger.info("First admin created")
        
    finally:
        db.close()
        
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    create_first_admin()
    