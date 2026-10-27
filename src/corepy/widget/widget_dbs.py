from sqlalchemy import Column, Integer, ForeignKey, String, UniqueConstraint, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from corepy.shared.mysql.base import Base

class WidgetsDB(Base):
    __tablename__ = "widgets"
    __table_args__ = (UniqueConstraint("site_id", "shortcode", name="uq_widgets_site_shortcode"),)
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    shortcode = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    site = relationship("SitesDB", back_populates="widgets")