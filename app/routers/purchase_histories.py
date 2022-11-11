"""
PurchaseHistory Router
"""
import re
from datetime import datetime
from pprint import pprint

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.services.purchase_histories import PurchaseHistoryService
from app.utils.database import get_db_session
from app.utils.security import require_auth

router = APIRouter()


@router.get("/")
async def get_purchase_histories_total(
    from_date: datetime = Query(None, description="from date"),
    to_date: datetime = Query(None, description="to date"),
    _: str = Depends(require_auth),
    db: Session = Depends(get_db_session),
):
    """
    Get purchase_histories total
    """
    purchase_histories_service = PurchaseHistoryService(db)
    purchase_histories = purchase_histories_service.get_purchase_histories(
        from_date=from_date, to_date=to_date
    )
    result = {
        "total_mask": 0,
        "total_amount": 0,
    }

    regex = r"^(?P<name>.+?)\s\((?P<color>.+?)\)\s\((?P<quantity>.+?)\sper\spack\)$"
    for purchase_history in purchase_histories:
        match = re.match(regex, purchase_history.mask_name)
        if not match:
            continue
        result["total_mask"] += int(match.group("quantity"))
        result["total_amount"] += purchase_history.transaction_amount
    return {"message": "ok", "data": result}
