""" PurchaseHistory Schema """
from datetime import datetime

from pydantic import BaseModel, Field


class ImportPurchaseHistory(BaseModel):
    """Purchase history data from json file"""

    mask_name: str = Field(..., alias="maskName")
    pharmacy_name: str = Field(..., alias="pharmacyName")
    transaction_amount: float = Field(..., alias="transactionAmount")
    transaction_date: datetime = Field(..., alias="transactionDate")


class PurchaseHistoryCreate(BaseModel):
    """Purchase history schema for create"""

    user_id: int
    mask_name: str = Field(..., alias="maskName")
    pharmacy_name: str = Field(..., alias="pharmacyName")
    transaction_amount: float = Field(..., alias="transactionAmount")
    transaction_date: datetime = Field(..., alias="transactionDate")


class PurchaseHistory(PurchaseHistoryCreate):
    """Purchase history schema in app"""

    id: int

    class Config:
        """Config for orm_mode"""

        orm_mode = True
