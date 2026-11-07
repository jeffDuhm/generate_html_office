from sqlalchemy import Column, Integer, ForeignKey, String, UniqueConstraint, DateTime, func
from sqlalchemy.orm import relationship
from corepy.shared.mysql.base import Base

class WidgetMatchesDB(Base):
    __tablename__ = "widget_matches"
    __table_args__ = (UniqueConstraint("widget_id", "user_id", "text", name="uq_widget_matches_user"),)
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    widget_id = Column(Integer, ForeignKey("widgets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(String(255), nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    widget = relationship("WidgetsDB", back_populates="matches")
    user = relationship("UsersDB", back_populates="widget_matches")