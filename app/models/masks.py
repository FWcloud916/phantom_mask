""" Mask DB Model """
from datetime import datetime

from sqlalchemy import (
    Column,
    Computed,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import TSVectorType

from app.utils.database import Base


class Mask(Base):
    """Mask database model"""

    __tablename__ = "masks"

    id = Column(Integer, primary_key=True, index=True)
    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id"))
    name = Column(String)
    color = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    name_tsv = Column(
        "name_tsv",
        TSVectorType("name"),
        Computed("to_tsvector('simple', \"name\")", persisted=True),
    )

    pharmacy = relationship("Pharmacy", back_populates="masks", cascade="all, delete")  # type: ignore

    __table_args__ = (
        # Indexing the TSVector column
        Index("idx_masks_name_tsv", name_tsv, postgresql_using="gin"),
    )
