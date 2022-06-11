from typing import Dict

from fastapi import FastAPI

app = FastAPI(title="Star-dust")


@app.get("/hello")
def hello_endpoint() -> Dict[str, str]:
    return {"greeting": "Hello"}
