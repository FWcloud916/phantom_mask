from enum import Enum


class SortOrder(str, Enum):
    """Sort order option"""

    asc = "asc"
    desc = "desc"


class CompareType(str, Enum):
    """Compare type option"""

    gt = "gt"
    lt = "lt"
