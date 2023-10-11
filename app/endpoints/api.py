from fastapi import APIRouter

from app.endpoints import v1

v1_router = APIRouter()

v1_router.include_router(v1.user.router, prefix="/user", tags=["User"])
v1_router.include_router(v1.auth.router, prefix="/auth", tags=["Auth"])
v1_router.include_router(v1.file.router, prefix="/file", tags=["File"])
