from fastapi import Depends
from sqlalchemy.orm import Session
from app.auth.models import User
from app.db import get_db
from . import crud, schemas

async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post, author_id=current_user.id)