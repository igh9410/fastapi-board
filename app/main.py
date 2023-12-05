from dotenv import load_dotenv
from fastapi import FastAPI

from app.db import init_db
from .router import router as app_router

app = FastAPI()

app.include_router(app_router)

load_dotenv() ## Load .env file

init_db()

@app.get("/")
async def root():
    return {"message": "Hello World"}
