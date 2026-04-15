from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.repositories.user_repository_mock import UserRepositoryMock
from app.services.auth_service import AuthService


class LoginRequestDTO(BaseModel):
    email: str
    password: str


router = APIRouter()
auth_service = AuthService(UserRepositoryMock())


@router.post("/login")
def login(request: LoginRequestDTO):
    try:
        token = auth_service.login(request.email, request.password)

        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
