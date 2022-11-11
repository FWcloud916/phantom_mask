from typing import TYPE_CHECKING, Optional

from pydantic import AnyHttpUrl, BaseModel, conint


class BaseResponse(BaseModel):
    """Base Response"""

    message: str

    class Config:
        """Config for BaseResponse"""

        extra = "forbid"


if TYPE_CHECKING:

    class BasePagination(BaseModel):
        """Base Pagination"""

        current_page: int
        first_page_url: AnyHttpUrl
        last_page: int
        last_page_url: AnyHttpUrl
        next_page_url: Optional[AnyHttpUrl]
        path: str
        per_page: int
        prev_page_url: Optional[AnyHttpUrl]
        to: Optional[int]
        total: int

else:

    class BasePagination(BaseModel):
        """Base Pagination"""

        current_page: conint(ge=1)
        first_page_url: AnyHttpUrl
        last_page: conint(ge=1)
        last_page_url: AnyHttpUrl
        next_page_url: Optional[AnyHttpUrl]
        path: str
        per_page: int
        prev_page_url: Optional[AnyHttpUrl]
        to: Optional[int]
        total: conint(ge=0)


"""
{
  "message": "fetch user success",
  "data": {
    "current_page": 1,
    "data": [
      {
        "id": "7d209887-d649-443c-a07f-344c5c27600d",
        "email": "admin@example.com",
        "name": "admin",
        "is_active": true,
        "is_superuser": true,
        "created": "2020-03-07 02:11:35",
        "updated": "2020-03-07 02:11:35"
      }
    ],
    "first_page_url": "http://localhost:8080/api/v1/user?page=1",
    "from": 1,
    "last_page": 3,
    "last_page_url": "http://localhost:8080/api/v1/user?page=3",
    "next_page_url": "http://localhost:8080/api/v1/user?page=2",
    "path": "http://localhost:8080/api/v1/user",
    "per_page": "1",
    "prev_page_url": null,
    "to": 1,
    "total": 3
  }
}
"""
