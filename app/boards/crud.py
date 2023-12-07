import logging
from typing import Tuple, Union
from uuid import UUID
from sqlalchemy import delete, desc, func, select, update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas
from app.posts import models as post_models

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
    
def get_board_list_crud(db: Session, user_id: UUID, page_number: int, page_size: int, sort: bool) -> Union[schemas.BoardList, Tuple[None, str]]:
    
    try:
        # Calculate offset for pagination
        offset = (page_number - 1) * page_size

        # Create a subquery for counting posts in each board
        posts_count_subquery = (
            select(post_models.Post.board_id, func.count(post_models.Post.id).label('post_count')) # Count the number of posts in each board by only fetching the post id, not entire post
            .group_by(post_models.Post.board_id)
            .subquery()
        )
        
        if sort: # Sort by post count
            order_clause = desc(func.coalesce(posts_count_subquery.c.post_count, 0)) # Use coalesce to return 0 if the post count is null
        else:
            order_clause = None
     

        # Main query to fetch boards with post count and apply access control
        boards_query = (
            select(models.Board, func.coalesce(posts_count_subquery.c.post_count, 0).label('post_count'))  # Use coalesce to return 0 if the post count is null
            .outerjoin(posts_count_subquery, models.Board.id == posts_count_subquery.c.board_id)
            .filter((models.Board.creator == user_id) | (models.Board.public == True))
            .order_by(order_clause)
            .offset(offset)
            .limit(page_size)
        )
        boards = db.execute(boards_query).all()

        # Map the result to your schemas
        board_list = [schemas.BoardGetWithPostCount(id=board.id, name=board.name, public=board.public, post_count=post_count) for board, post_count in boards]

        # Total count of boards accessible by the user
        total_boards_query = select(func.count()).select_from(models.Board).filter((models.Board.creator == user_id) | (models.Board.public == True))
        total_boards = db.execute(total_boards_query).scalar()

        return schemas.BoardList(
            boards=board_list,
            pagination=schemas.Pagination(
                page_number=page_number,
                page_size=page_size,
                total_items=total_boards,
                total_pages=(total_boards + page_size - 1) // page_size
            )
        )
    except Exception as e:
        # Log the exception and return an error message
        logging.exception('An exception occurred while retrieving boards: %s', e)
        return None, "Failed to retrieve boards"

