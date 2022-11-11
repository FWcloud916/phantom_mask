"""
user routers
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request

from app.models.purchase_histories import PurchaseHistory
from app.models.users import User as UserModel
from app.schemas.users import AuthIn, AuthOut, User, UserOut
from app.services.users import UserService
from app.utils.config import settings
from app.utils.database import get_db_session
from app.utils.security import require_auth

router = APIRouter()


@router.get("/")
async def get_users(
    _: str = Depends(require_auth), db: Session = Depends(get_db_session)
):
    """
    get all users
    """
    user_service = UserService(db)
    users = user_service.get_users()
    return {"message": "get users success", "data": users}


@router.get("/{user_id}")
async def get_user(
    user_id: int, _: str = Depends(require_auth), db: Session = Depends(get_db_session)
):
    """
    get user by id
    """
    user_service = UserService(db)
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    purchase_histories = [jsonable_encoder(h) for h in user.purchase_histories]
    # result = User(**{
    #     "id": user.id,
    #     "name": user.name,
    #     "email": user.email,
    #     "purchase_histories": purchase_histories
    # })
    return {"message": "get user success", "data": purchase_histories}
