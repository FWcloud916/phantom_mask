""" PurchaseHistory DB Model """
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.utils.database import Base


class PurchaseHistory(Base):
    """Purchase history data from json file"""

    __tablename__ = "purchase_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    mask_name = Column(String, nullable=False)
    pharmacy_name = Column(String, nullable=False)
    transaction_amount = Column(Float, default=0)
    transaction_date = Column(DateTime, default=datetime.now)

    user = relationship(
        "User", back_populates="purchase_histories", cascade="all, delete"
    )
