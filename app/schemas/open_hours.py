""" OpenHours Schema"""
from enum import Enum, IntEnum

from pydantic import BaseModel


class OpenHoursDay(IntEnum, Enum):
    """Open hours day"""

    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6
    SUN = 0


class OpenHoursCreate(BaseModel):
    """Open hours"""

    day: OpenHoursDay
    open_time: str | None
    close_time: str | None


class OpenHours(OpenHoursCreate):
    """Open hours"""

    id: int
    pharmacy_id: int

    class Config:
        """Config for orm_mode"""

        orm_mode = True
