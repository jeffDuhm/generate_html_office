from sqlalchemy import String, Column, func, Boolean, DateTime, Integer
from sqlalchemy.orm import relationship
from corepy.shared.mysql.base import Base

class SitesDB(Base):
    __tablename__ = "sites"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    widgets = relationship("WidgetsDB", back_populates="site")