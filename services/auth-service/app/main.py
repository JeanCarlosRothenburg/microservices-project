from fastapi import FastAPI
from app.controller.auth_controller import router as auth_router

app = FastAPI(root_path="/auth")

app.include_router(auth_router)
