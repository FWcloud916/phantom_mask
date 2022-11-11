"""User CURD service"""
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.users import User as UserModel
from app.schemas.users import UserCreate
from app.services.service import BaseService
from app.utils.config import settings
class UserService(BaseService):
    """User CURD service"""

    def __init__(self, db: Session):
        super().__init__(db)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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

