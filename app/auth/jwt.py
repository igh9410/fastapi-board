from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from app.config import settings 
from datetime import datetime, timedelta
import uuid
import jwt
from pydantic import BaseModel
from .security import verify_password
from . import crud
from sqlalchemy.orm import Session


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
    
    if expires_delta: # Token expiration time during route creation
        expire = datetime.utcnow() + expires_delta
    else: # Token expiration time not provided, set default time to 15 mins
        expire = datetime.utcnow() + timedelta(15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def authenticate_user(db:Session, email: str, password: str):   
    user = crud.get_user_by_email(db, email)
    if not user or verify_password(password, user.password) == False:
        return False
    return user

def validate_jwt_token(authorization: HTTPAuthorizationCredentials = settings.SECURITY):
    try:
        token = authorization.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])     
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error with the token provided")




