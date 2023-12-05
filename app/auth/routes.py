from app.config import settings
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, security, status
import jwt
from sqlalchemy.orm import Session
from app.auth.jwt import LoginRequest, authenticate_user, create_access_token
from . import crud, schemas
from app.db import get_db
from app.redis import redis_client


async def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

async def login_for_access_token(login_request: LoginRequest, db: Session = Depends(get_db)):  
    user = authenticate_user(db, login_request.email, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(days=7))
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

async def logout(credentials: security.HTTPAuthorizationCredentials = Depends(settings.SECURITY)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]) # Decode token
        expiration_time:int = payload.get("exp")
        current_time = datetime.utcnow()
        remaining_time = expiration_time - int(current_time.timestamp())
      
        if remaining_time > 0: ## Check if token is still valid
            redis_client.setex(token, timedelta(seconds=remaining_time), "denied")
            return {"message": "Logged out successfully"}
        
    except jwt.ExpiredSignatureError:
        return {"message": "Token already expired"}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



   
