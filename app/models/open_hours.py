""" OpenHours DB Model """
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.utils.database import Base


class OpenHours(Base):
    """OpenHours database model"""

    __tablename__ = "open_hours"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Integer)
    open_time = Column(String)
    close_time = Column(String)
    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id"))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    pharmacy = relationship(
        "Pharmacy", back_populates="open_hours", cascade="all, delete"  # type: ignore
    )
