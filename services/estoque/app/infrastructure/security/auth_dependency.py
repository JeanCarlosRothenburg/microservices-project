from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.infrastructure.security.token_validator import validate_token

security = HTTPBearer()


def get_current_user():
    return {"email": "dev@local.com"}
