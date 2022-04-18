from fastapi import FastAPI

app = FastAPI(title="Star-dust")


@app.get("/hello")
def hello_endpoint():
    return {"greeting": "Hello"}
