from fastapi import Depends
from sqlalchemy.orm import Session
from app.auth.models import User
from app.auth.security import get_current_user
from app.db import get_db
from . import crud, schemas

async def create_post_route(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_post_crud(db=db, post=post, author_id=current_user.id)