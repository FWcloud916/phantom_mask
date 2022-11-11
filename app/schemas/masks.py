""" Mask Schema"""
from enum import Enum

from pydantic import BaseModel


class ImportMask(BaseModel):
    """Mask schema for import json"""

    name: str
    price: float


class MaskCreate(BaseModel):
    """Mask schema for create"""

    name: str
    color: str
    quantity: int
    price: float


class Mask(MaskCreate):
    """Mask schema in app"""

    id: int
    pharmacy_id: int

    class Config:
        """Config for orm_mode"""

        orm_mode = True


class MaskSortBy(str, Enum):
    """Mask sort by"""

    name: str = "name"
    price: str = "price"
