import os
from datetime import datetime, timedelta
import uuid
from fastapi import Depends
import jwt
from pydantic import BaseModel
from app import db
from . import crud
from sqlalchemy.orm import Session

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "UYaGFRTeAJ_q5psBZMwBNJhWVKmDYn3I4SicIxk7D_8=")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    for key, value in to_encode.items():
        if isinstance(value, uuid.UUID):
            to_encode[key] = str(value)

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db:Session, email: str, password: str):
    # Implement your user authentication logic here
    # For example: 
    user = crud.get_user_by_email(db, email)
    if not user or crud.verify_password(password, user.password) == False:
        print("user password: ", user.password)
        print("password: ", password) 
        return False
    return user


