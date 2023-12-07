from uuid import UUID
from fastapi import Depends, HTTPException, Query,status
from sqlalchemy.orm import Session
from app.auth.security import get_current_user
from app.db import get_db
from . import models, crud, schemas

async def create_post_route(board_id: UUID, post: schemas.PostCreate, db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)) -> schemas.PostCreate:
    user_uuid = UUID(current_user_id)
    created_post = crud.create_post_crud(db=db, board_id=board_id, post=post, author_id=user_uuid)
    
    if isinstance(created_post, models.Post):
        # Successful creation, returning the response
        response = schemas.PostCreate(title=created_post.title, content=created_post.content)
        return response
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User have no access to the board")
    

async def update_post_route(board_id: UUID, post_id: UUID, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)) -> schemas.PostUpdate:
    user_uuid = UUID(current_user_id)
    
    updated_post = crud.update_post_crud(db=db, board_id=board_id, post_id=post_id, post=post, author_id=user_uuid)
    
    if isinstance(updated_post, models.Post):
        # Successful update, returning the response
        response = schemas.PostUpdate(title=updated_post.title, content=updated_post.content)    
        return response
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found or update not allowed")
    
async def delete_post_route(board_id: UUID, post_id: UUID, db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)):
    user_uuid = UUID(current_user_id)
    try:
        crud.delete_post_crud(db=db, board_id=board_id, post_id=post_id, author_id=user_uuid)
        return {"message": "Post deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found or delete not allowed") from e

async def get_post_route(board_id: UUID, post_id: UUID, db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)) -> schemas.PostGet:
    user_uuid = UUID(current_user_id)
    
    fetched_post = crud.get_post_crud(db=db, board_id=board_id, post_id=post_id, author_id=user_uuid)
    
    if isinstance(fetched_post, models.Post):
        # Successful creation, returning the response
        response = schemas.PostGet(title=fetched_post.title, content=fetched_post.content)
        return response
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found or retrieving not allowed")

async def get_post_list_route(board_id: UUID, page_number: int = Query(1, alias="page_number"),
    page_size: int = Query(20, alias="page_size"), db: Session = Depends(get_db), current_user_id: str = Depends(get_current_user)) -> schemas.PostList:
    user_uuid = UUID(current_user_id)

    post_list = crud.get_post_list_crud(db=db, board_id=board_id, user_id=user_uuid, page_number=page_number, page_size=page_size) # Set default page size to 20
    if isinstance(post_list, schemas.PostList):
       return post_list
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts not found or retrieving not allowed")