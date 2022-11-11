"""
Leaderboard info api
"""
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.services.users import UserService
from app.utils.database import get_db_session
from app.utils.security import require_auth

router = APIRouter()


@router.get("/users")
async def get_user_leaderboard(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0),
    from_date: datetime = Query(None, description="from date"),
    to_date: datetime = Query(None, description="to date"),
    _: str = Depends(require_auth),
    db: Session = Depends(get_db_session),
):
    """
    Get user leaderboard
    """
    user_service = UserService(db)
    users = user_service.get_top_balance_users(
        skip=skip, limit=limit, from_date=from_date, to_date=to_date
    )

    return {"message": "ok", "data": users}
