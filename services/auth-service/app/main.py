import os
from fastapi import FastAPI
from app.controller.auth_controller import router as auth_router

swagger_enabled = os.getenv("SWAGGER_ENABLED", "true").lower() == "true"

app = FastAPI(
    root_path="/auth",
    docs_url="/docs" if swagger_enabled else None,
    redoc_url="/redoc" if swagger_enabled else None,
    openapi_url="/openapi.json" if swagger_enabled else None,
)

app.include_router(auth_router)
