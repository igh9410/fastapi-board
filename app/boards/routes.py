from uuid import UUID
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.boards import models
from app.auth.security import get_current_user
from app.db import get_db
from . import crud, schemas

async def create_board_route(board: schemas.BoardCreate, db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)) -> schemas.BoardCreate:
    user_uuid = UUID(current_user_id)
    created_board = crud.create_board_crud(db=db, board=board, user_id=user_uuid)

    if isinstance(created_board, models.Board):
        # Successful creation, returning the response
        response = schemas.BoardCreate(name=created_board.name, public=created_board.public)    
        return response            
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A board with that name already exists")
    
    

async def update_board(id: UUID, board: schemas.BoardUpdate, db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)) -> schemas.BoardUpdate:
    user_uuid = UUID(current_user_id)
    
    updated_board = crud.update_board_crud(db=db, board_id=id, board=board, user_id=user_uuid)

    if isinstance(updated_board, models.Board):
        # Successful creation, returning the response
        response = schemas.BoardUpdate(name=updated_board.name, public=updated_board.public)    
        return response
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found or update not allowed") 
    
async def delete_board_route(id: UUID, db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)) -> dict:
    user_uuid = UUID(current_user_id)
    try:
        crud.delete_board_crud(db=db, board_id=id, user_id=user_uuid)
        return {"message": "Board deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found or delete not allowed") from e
    
async def get_board_route(id: UUID, db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)) -> schemas.BoardGet:
    user_uuid = UUID(current_user_id)

    fetched_board = crud.get_board_crud(db=db, board_id=id, user_id=user_uuid)

    if isinstance(fetched_board, models.Board):
        # Successful creation, returning the response
        response = schemas.BoardGet(name=fetched_board.name, public=fetched_board.public)    
        return response
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found or retrieving not allowed") 
    
async def get_board_list_route(db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)) -> schemas.BoardList:
    user_uuid = UUID(current_user_id)
    try:
        board_list = crud.get_board_list_crud(db=db, user_id=user_uuid)
        return board_list
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found or retrieving not allowed") from e