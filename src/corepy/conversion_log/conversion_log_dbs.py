from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from corepy.shared.mysql.base import Base

class ConversionLogsDB(Base):
    __tablename__ = "conversion_logs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    filename = Column(String(150), nullable=False)
    error_message = Column(Text, nullable=True)
    status = Column(String(20), nullable=False)
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )

    user = relationship("UsersDB", back_populates="conversion_logs")
    site = relationship("SitesDB", back_populates="conversion_logs")
    