from datetime import timedelta
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import schemas
from app.auth.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, LoginRequest, Token, authenticate_user, create_access_token

from app.db import init_db
from .router import router as app_router

app = FastAPI()

app.include_router(app_router)

load_dotenv() ## Load .env file

init_db()

@app.get("/")
async def root():
    return {"message": "Hello World"}
