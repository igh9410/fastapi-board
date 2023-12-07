from uuid import UUID
from fastapi import Depends, HTTPException, Query, status
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
    
    

async def update_board_route(id: UUID, board: schemas.BoardUpdate, db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)) -> schemas.BoardUpdate:
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
        response = schemas.BoardGet(id=fetched_board.id,name=fetched_board.name, public=fetched_board.public)    
        return response
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found or retrieving not allowed") 
    
async def get_board_list_route(page_number: int = Query(1, alias="page_number"),
    page_size: int = Query(20, alias="page_size"), sort: bool = Query(False, alias="sort"), db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)) -> schemas.BoardList: # if sort is true, sort by post counts in descending order
    user_uuid = UUID(current_user_id)
    board_list = crud.get_board_list_crud(db=db, user_id=user_uuid, sort=sort, page_number=page_number, page_size=page_size) # Set default page size to 20
    
    if isinstance(board_list, schemas.BoardList):
       return board_list
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Boards not found or retrieving not allowed")
    