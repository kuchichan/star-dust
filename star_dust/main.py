from typing import Dict

from fastapi import FastAPI

from star_dust.api.api_v1.api import api_router

app = FastAPI(title="Star-dust")
app.include_router(api_router, prefix="/")


@app.get("/hello")
def hello_endpoint() -> Dict[str, str]:
    return {"greeting": "Hello"}
