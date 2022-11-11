""" Pharmacy schemas """
from fastapi import Query
from pydantic import BaseModel, Field

from app.schemas.masks import ImportMask, Mask
from app.schemas.open_hours import OpenHours, OpenHoursDay


class ImportPharmacy(BaseModel):
    """Pharmacy data from json file"""

    name: str
    cash_balance: float = Field(..., alias="cashBalance")
    open_hours: str = Field(..., alias="openingHours")
    masks: list[ImportMask]


class PharmacyCreate(BaseModel):
    """Pharmacy"""

    name: str
    cash_balance: float


class Pharmacy(PharmacyCreate):
    """Pharmacy"""

    id: int
    open_hours: list[OpenHours] = []
    masks: list[Mask] = []

    class Config:
        """Config for orm_mode"""

        orm_mode = True


class PharmacyIn(BaseModel):
    """Pharmacy schema for response"""

    day: OpenHoursDay | None = Query(None, title="Day of week")
    open_time: str = Query(
        None,
        regex=r"^(?:[01]\d|2[0-3]):[0-5]\d$",
        title="Open time",
        example="08:00",
        description="Open time format: HH:MM",
    )
    close_time: str = Query(
        None,
        regex=r"^(?:[01]\d|2[0-3]):[0-5]\d$",
        title="Close time",
        example="17:00",
        description="Close time format: HH:MM",
    )
