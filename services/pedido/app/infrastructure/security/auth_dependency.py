from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.infrastructure.security.token_validator import validate_token

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = validate_token(token)
        return payload
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))