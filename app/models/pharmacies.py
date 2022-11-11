""" Pharmacy DB Model """
from datetime import datetime

from sqlalchemy import Column, Computed, DateTime, Float, Index, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import TSVectorType

from app.models.masks import Mask
from app.models.open_hours import OpenHours
from app.utils.database import Base


class Pharmacy(Base):
    """Pharmacy database model"""

    __tablename__ = "pharmacies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    cash_balance = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    name_tsv = Column(
        TSVectorType("name"),
        Computed("to_tsvector('simple', \"name\")", persisted=True),
    )
    open_hours = relationship(
        OpenHours, back_populates="pharmacy", cascade="all, delete"
    )
    masks = relationship(Mask, back_populates="pharmacy", cascade="all, delete")

    __table_args__ = (
        # Indexing the TSVector column
        Index("idx_pharmacies_name_tsv", name_tsv, postgresql_using="gin"),
    )
