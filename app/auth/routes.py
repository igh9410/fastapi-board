from fastapi import Depends, HTTPException, Response, status, Request
from sqlalchemy.orm import Session
from app.auth.utils import create_unique_token
from app.auth.security import LoginRequest, authenticate_user
from app.auth import crud, schemas
from app.db import get_db
from app.redis import redis_client


async def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


async def login(
    request: Request,
    response: Response,
    login_request: LoginRequest,
    db: Session = Depends(get_db),
) -> schemas.Token:
    user = authenticate_user(db, login_request.email, login_request.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    existing_session_token = request.cookies.get(
        "session_token"
    )  # get session token from cookies

    if existing_session_token is not None:
        request.cookies.pop("session_token")  # Removes session token from cookies

    session_token = create_unique_token()
    redis_client.set(
        session_token, str(user.id), ex=604800
    )  # set session token in redis, expiration time is 7 days

    response.set_cookie(
        key="session_token",
        value=session_token,
        expires=604800,
        httponly=True,
        secure=True,
    )  # Cookie expires after 7 days, httponly and secure flags are set

    return schemas.Token(access_token=session_token)


async def logout(request: Request, response: Response):
    session_token = request.cookies.get("session_token")

    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token not found in cookies",
        )
    redis_client.delete(
        str(request.cookies.get("session_token"))
    )  # Removes session token from redis

    response.delete_cookie(key="session_token")  # Removes session token from cookies
