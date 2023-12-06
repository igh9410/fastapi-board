import logging
from typing import Tuple, Union
from uuid import UUID
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from . import models, schemas

def create_board_crud(db: Session, board: schemas.BoardCreate, user_id: UUID) -> Union[models.Board, Tuple[None, str]]:
    try:
        db_board = models.Board(name=board.name, public=board.public, creator=user_id)
        db.add(db_board)
        db.commit()
        db.refresh(db_board)
        return db_board       
    except IntegrityError:
        db.rollback()  # Rollback the transaction
        return None, "A Board with that name already exists"
    

def update_board_crud(db: Session, board_id: UUID, board: schemas.BoardUpdate, user_id: UUID) -> Union[models.Board, Tuple[None, str]]:
    # Fetch the board's creator and public status
    try:
        stmt = select(models.Board).where(models.Board.id == board_id)
        result = db.execute(stmt)    
        db_board = result.scalars().first()

        if db_board is None:
            return None, "Board not found"  
   
        if db_board.creator != user_id:
            return None, "Only the board's creator can update it"
    
        # Update the board
        update_stmt = (
            update(models.Board)
            .where(models.Board.id == board_id)
            .values(name=board.name, public=board.public)
        )

        db.execute(update_stmt)
        db.commit()
        db.refresh(db_board)

    except Exception:
        db.rollback()       
        return None, "Database error occurred while updating the board"
      
    return db_board

def delete_board_crud(db: Session, board_id: UUID, user_id: UUID) -> None:
    # Fetch the board's creator and public status
    stmt = select(models.Board).where(models.Board.id == board_id)
    result = db.execute(stmt)    
    db_board = result.scalars().first()
    
    if db_board is None:
        raise ValueError("Board not found")
    if db_board.creator != user_id:
        raise ValueError("Only the board's creator can delete it")
    
    # Delete the board
    delete_stmt = (
        delete(models.Board)
        .where(models.Board.id == board_id)
    )

    db.execute(delete_stmt)
    db.commit()
    
    return None

def get_board_crud(db: Session, board_id: UUID, user_id: UUID) -> Union[models.Board, Tuple[None, str]]:
    # Fetch the board's creator and public status
  
    stmt = select(models.Board).where(models.Board.id == board_id)
    result = db.execute(stmt)    
    db_board = result.scalars().first()

    if db_board is None:
        return None, "Board not found"
    
    if db_board.public: ## If the board is public, anyone can view it
        return db_board  

    if db_board.creator != user_id:
        return None, "Only the board's creator can access it"    
        
    return db_board ## If the board is private, only the creator can view it
    
    


