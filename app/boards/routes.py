from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session
from app.auth.security import get_current_user
from app.db import get_db
from . import crud, schemas

async def create_board(board: schemas.BoardCreate, db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    user_uuid = UUID(current_user_id)  # Convert the string to a UUID
    return crud.create_board(db=db, board=board, user_id=user_uuid)