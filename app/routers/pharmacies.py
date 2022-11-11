"""
Pharmacy routers
"""
from pprint import pprint

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schemas.masks import MaskSortBy
from app.schemas.open_hours import OpenHoursDay
from app.schemas.pharmacies import Pharmacy, PharmacyIn
from app.schemas.query import CompareType, SortOrder
from app.services.masks import MaskService
from app.services.pharmacies import PharmacyService
from app.utils.database import get_db_session
from app.utils.security import require_auth

router = APIRouter()


@router.get("/")
async def get_pharmacies(
    _: str = Depends(require_auth),
    day: OpenHoursDay = Query(None),
    open_time: str = Query(
        None,
        regex=r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$",
        description="open time, format HH:mm",
        example="09:00",
    ),
    close_time: str = Query(
        None,
        regex=r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$",
        description="close time, format HH:mm",
        example="18:00",
    ),
    quantity: int = Query(None, gt=0, description="quantity of products"),
    compare_type: CompareType = Query(
        None,
        description="compare type, gt (greater than), lt (less than)",
        example="gt",
    ),
    max_price: float = Query(None, gt=0, description="max price of products"),
    min_price: float = Query(None, gt=0, description="min price of products"),
    db: Session = Depends(get_db_session),
):
    """
    get all pharmacies
    """
    pharmacy_service = PharmacyService(db)
    pharmacies = pharmacy_service.get_pharmacies(
        day=day,
        open_time=open_time,
        close_time=close_time,
        quantity=quantity,
        compare_type=compare_type,
        max_price=max_price,
        min_price=min_price,
    )
    data = [
        Pharmacy(
            **{
                "id": pharmacy.id,
                "name": pharmacy.name,
                "cash_balance": pharmacy.cash_balance,
                "open_hours": pharmacy.open_hours,
                "masks": pharmacy.masks,
            }
        )
        for pharmacy in pharmacies
    ]

    return {"message": "get pharmacies success", "data": data}


@router.get("/search")
async def search_pharmacies(
    query: str = Query(..., description="search query"),
    db: Session = Depends(get_db_session),
):
    """
    search pharmacies
    """
    pharmacy_service = PharmacyService(db)
    pharmacies = pharmacy_service.search_pharmacies_by_name(query=query)
    if not pharmacies:
        return {"message": "no pharmacies found", "data": []}
    data = [
        Pharmacy(
            **{
                "id": pharmacy.id,
                "name": pharmacy.name,
                "cash_balance": pharmacy.cash_balance,
                "open_hours": pharmacy.open_hours,
                "masks": pharmacy.masks,
            }
        )
        for pharmacy in pharmacies
    ]

    return {"message": "search pharmacies success", "data": data}


@router.get("/{pharmacy_id}/masks")
async def get_pharmacy_masks(
    pharmacy_id: int,
    _: str = Depends(require_auth),
    sort_by: MaskSortBy = Query(
        description="sort by name or price", default=MaskSortBy.price
    ),
    sort_order: SortOrder = Query(
        description="sort order asc or desc", default=SortOrder.desc
    ),
    db: Session = Depends(get_db_session),
):
    """
    get all masks of pharmacy
    """
    mask_service = MaskService(db)
    masks = mask_service.get_masks_by_pharmacy_id(
        pharmacy_id, sort_by=sort_by, sort_order=sort_order
    )
    return {"message": "get masks success", "data": masks}
