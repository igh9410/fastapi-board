from uuid import UUID
from sqlalchemy.orm import Session
from . import models, schemas

def create_board(db: Session, board: schemas.BoardCreate, user_id: UUID):
    db_board = models.Board(name=board.name, public=board.public, creator=user_id)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board