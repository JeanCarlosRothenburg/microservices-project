from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel
import jwt
import os

from app.repositories.user_repository_mock import UserRepositoryMock
from app.services.auth_service import AuthService
from app.infrastructure.security.token_validator import validate_token

class LoginRequestDTO(BaseModel):
    email: str
    password: str

router = APIRouter()
auth_service = AuthService(UserRepositoryMock())
JWT_SECRET = os.getenv("JWT_SECRET")

@router.post("/login")
def login(request: LoginRequestDTO):
    try:
        token = auth_service.login(request.email, request.password)

        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/validate")
def validate(request: Request):
    auth = request.headers.get("Authorization")

    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401)

    token = auth.split(" ")[1]

    try:
        payload = validate_token(token)
        return Response(status_code=200, headers={"X-User-Id": str(payload.get("sub"))})
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")