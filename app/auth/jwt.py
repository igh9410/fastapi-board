import os
from datetime import datetime, timedelta
import uuid
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from pydantic import BaseModel
from app import db
from . import crud
from sqlalchemy.orm import Session


# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "UYaGFRTeAJ_q5psBZMwBNJhWVKmDYn3I4SicIxk7D_8=")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECURITY = HTTPBearer()

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    for key, value in to_encode.items(): # Convert UUID to string
        if isinstance(value, uuid.UUID):
            to_encode[key] = str(value)

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db:Session, email: str, password: str):   
    user = crud.get_user_by_email(db, email)
    if not user or crud.verify_password(password, user.password) == False:
        return False
    return user

def validate_jwt_token(authorization: HTTPAuthorizationCredentials = SECURITY):
    try:
        token = authorization.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])     
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error with the token provided")


