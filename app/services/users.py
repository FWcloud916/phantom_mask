"""User CURD service"""
from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.purchase_histories import PurchaseHistory as PurchaseHistoryModel
from app.models.users import User as UserModel
from app.schemas.users import UserCreate
from app.services.service import BaseService
from app.utils.config import settings


class UserService(BaseService):
    """User CURD service"""

    def __init__(self, db: Session):
        super().__init__(db)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_user(self, user_id: int):
        """Get user by id"""
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_user_by_email(self, email: str):
        """Get user by email"""
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100):
        """Get users"""
        return self.db.query(UserModel).offset(skip).limit(limit).all()

    def get_top_balance_users(
        self,
        skip: int = 0,
        limit: int = 100,
        from_date: datetime = None,
        to_date: datetime = None,
    ):
        """Get top users"""
        query = (
            self.db.query(
                UserModel,
                func.sum(PurchaseHistoryModel.transaction_amount).label("total_amount"),
            )
            .join(PurchaseHistoryModel)
            .group_by(UserModel.id)
            .order_by(desc("total_amount"))
        )
        if from_date:
            query = query.filter(
                UserModel.purchase_histories.any(
                    PurchaseHistoryModel.transaction_date >= from_date
                )
            )
        if to_date:
            query = query.filter(
                UserModel.purchase_histories.any(
                    PurchaseHistoryModel.transaction_date <= to_date
                )
            )
        return query.offset(skip).limit(limit).all()

    def create_user(self, user: UserCreate):
        """Create user"""
        db_user = UserModel(
            name=user.name,
            email=user.email,
            hashed_password=self.get_password_hash(user.password),
            cash_balance=user.cash_balance,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def verify_password(self, plain_password: str, hashed_password: str):
        """Verify password"""
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """Get password hash"""
        return self.pwd_context.hash(password)

    @staticmethod
    def create_access_token(user: UserModel, expires_delta: timedelta = None) -> str:
        """Create access token"""
        to_encode = {"sub": user.email}
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt
