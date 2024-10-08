from fastapi import APIRouter
from app.api.api_v1.endpoints import home

api_router = APIRouter()

api_router.include_router(home.router, prefix="", tags=["home"])
