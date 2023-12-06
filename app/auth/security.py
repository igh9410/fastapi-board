from fastapi import HTTPException, Request
from app.auth.models import User
from . import crud
from .utils import verify_password
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.redis import redis_client


async def get_current_user(request: Request) -> str:
    current_session_token = request.cookies.get("session_token")
    if not current_session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    current_user_id_bytes = redis_client.get(current_session_token) # get user id from redis
    if current_user_id_bytes is not None:
        current_user_id = current_user_id_bytes.decode('utf-8')  # Convert byte string to a regular string
    else:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return current_user_id

class LoginRequest(BaseModel):
    email: str
    password: str


def authenticate_user(db:Session, email: str, password: str):   
    user = crud.get_user_by_email(db, email)
    if not user or verify_password(password, user.password) == False:
        return False
    return user

