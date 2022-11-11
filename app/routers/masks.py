"""
Mask Router
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.services.masks import MaskService
from app.utils.database import get_db_session
from app.utils.security import require_auth

router = APIRouter()


@router.get("/search")
async def search_masks(
    query: str = Query(..., description="search query"),
    _: str = Depends(require_auth),
    db: Session = Depends(get_db_session),
):
    """
    search masks
    """
    mask_service = MaskService(db)
    masks = mask_service.search_masks_by_name(query=query)
    if not masks:
        return {"message": "no masks found", "data": []}
    return {"message": "search masks success", "data": masks}
