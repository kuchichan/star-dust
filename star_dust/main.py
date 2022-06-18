from fastapi import FastAPI

from star_dust.api.api_v1.api import api_router
from star_dust.core.config import settings

app = FastAPI(title="Star-Dust", openapi_url=f"{settings.api_v1_str}/openapi.json")
app.include_router(api_router, prefix=settings.api_v1_str)
