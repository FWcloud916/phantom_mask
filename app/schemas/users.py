""" User Schema"""
from pydantic import BaseModel, Field

from app.schemas.purchase_histories import ImportPurchaseHistory, PurchaseHistory


class ImportUser(BaseModel):
    """User data from json file"""

    name: str
    cash_balance: float = Field(..., alias="cashBalance")
    purchase_histories: list[ImportPurchaseHistory] = Field(
        ..., alias="purchaseHistories"
    )


class UserBase(BaseModel):
    """User schema for create and update"""

    name: str
    email: str
    cash_balance: float = Field(default=0)


class UserCreate(UserBase):
    """User schema for create"""

    password: str


class User(UserBase):
    """User schema in app"""

    id: int
    is_active: bool
    purchase_histories: list[PurchaseHistory]

    class Config:
        """Config for orm_mode"""

        orm_mode = True


class UserOut(BaseModel):
    """User schema for response"""

    message: str
    data: User


class Token(BaseModel):
    """
    JWT Token schema
    """

    access_token: str
    token_type: str
    expires_in: int


class AuthIn(BaseModel):
    """Auth schema for login"""

    email: str
    password: str


class AuthOut(BaseModel):
    """Auth response schema"""

    message: str
    data: Token
