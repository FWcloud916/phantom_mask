"""
login router
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.schemas.users import AuthIn, AuthOut
from app.services.users import UserService
from app.utils.config import settings
from app.utils.database import get_db_session

router = APIRouter()


@router.post("/login", response_model=AuthOut)
async def login_access_token(auth: AuthIn, db: Session = Depends(get_db_session)):
    """
    login user
    """
    user_service = UserService(db)
    user = user_service.get_user_by_email(auth.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    hashed_pass = user.hashed_password
    if not user_service.verify_password(auth.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    return {
        "message": "login success",
        "data": {
            "access_token": user_service.create_access_token(user),
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        },
    }


@router.post("/token", response_model=AuthOut)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session),
):
    """
    login user
    """
    user_service = UserService(db)
    user = user_service.get_user_by_email(form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    hashed_pass = user.hashed_password
    if not user_service.verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    return {
        "message": "login success",
        "data": {
            "access_token": user_service.create_access_token(user),
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        },
    }
