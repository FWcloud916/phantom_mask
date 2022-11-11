"""
Dependencies for access control for different types of users
"""

from fastapi import Security
from fastapi.security import OAuth2PasswordBearer

REUSABLE_OAUTH2 = OAuth2PasswordBearer(tokenUrl="/token")


def require_auth(token: str = Security(REUSABLE_OAUTH2)):
    """Require authentication"""
    return token
