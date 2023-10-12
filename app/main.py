from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI

from app.core.config import settings
from app.endpoints.api import v1_router

app = FastAPI(
    title=f"[{settings.ENV.upper()}] {settings.TITLE}",
    debug=True if settings.ENV in ["dev", "staging"] else False,
    openapi_url=f"{settings.API_BASE_URL}/openapi.json"
    # responses={
    # }
)


app.add_middleware(DebugToolbarMiddleware, settings=[settings])


app.include_router(v1_router, prefix="/api/v1")
