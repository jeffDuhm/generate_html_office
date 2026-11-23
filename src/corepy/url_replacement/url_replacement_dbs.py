from sqlalchemy import Column, Integer, ForeignKey, String, UniqueConstraint, DateTime, func
from sqlalchemy.orm import relationship
from corepy.shared.mysql.base import Base

class UrlReplacementsDB(Base):
    __tablename__ = "url_replacements"
    __table_args__ = (UniqueConstraint("user_id", "site_id", "source_url"),)
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    source_url = Column(String(255), nullable=False)
    target_url = Column(String(255), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(),
        nullable=False
    )
    
    user = relationship("UsersDB", back_populates="url_replacements")
    site = relationship("SitesDB", back_populates="url_replacements")