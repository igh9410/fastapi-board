import logging
from typing import Tuple, Union
import uuid
from uuid import UUID
from sqlalchemy import delete, desc, func, select, update
from sqlalchemy.orm import Session

from . import models, schemas
from app.boards import models as board_models

def create_post_crud(db: Session, board_id: UUID, post: schemas.PostCreate, author_id: UUID) -> Union[models.Post, Tuple[None, str]]:
    # Check if the user has access to the board
    board_access = is_board_accessible(db=db, board_id=board_id, user_id=author_id)

    if not board_access: # Has no access to the board        
        return None, "Board not found or retrieving not allowed"
    
    # Generate a UUID v1 for the new post
    post_id = uuid.uuid1()
    
    try:
        db_post = models.Post(
            id=post_id,
            title=post.title, 
            content=post.content, 
            author_id=author_id, 
            board_id=board_id
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except Exception:
        db.rollback()
        logging.exception("Failed to create post due to database error")       
        return None, "Failed to create post due to database error"

def update_post_crud(db: Session, board_id: UUID, post_id: UUID, post: schemas.PostUpdate, author_id: UUID) -> Union[models.Post, Tuple[None, str]]:
    # Check if the user has access to the board
    board_access = is_board_accessible(db=db, board_id=board_id, user_id=author_id)
    
    if not board_access: # Has no access to the board
        return None, "Board not found or retrieving not allowed"
    
    try:
        stmt = select(models.Post).where(models.Post.id == post_id)
        result = db.execute(stmt)    
        db_post = result.scalars().first()

        if db_post is None:
            logging.info(f"Post {post_id} not found")
            return None, "Board not found"  

        if db_post.author_id != author_id:
            logging.info(f"User {author_id} is not the author of post {post_id}")
            return None, "Only the post's author can update it"
        
        update_values = {}
        if post.title is not None:
            update_values['title'] = post.title
        if post.content is not None:
            update_values['content'] = post.content


        # Update the board
        if update_values:
            update_stmt = (
                update(models.Post)
                .where(models.Post.id == post_id)
                .values(**update_values)
            )
            db.execute(update_stmt)
            db.commit()
            db.refresh(db_post)
        else:
            return None, "No update values provided"
    except Exception:
        db.rollback()       
        return None, "Database error occurred while updating the post"
    return db_post


def delete_post_crud(db: Session, board_id: UUID, post_id: UUID, author_id: UUID) -> None:
    # Fetch the post's author
    stmt = select(models.Post.author_id).where(models.Post.id == post_id)
    result = db.execute(stmt)    
    db_post = result.fetchone()

    if db_post is None:
        logging.info(f"Post {post_id} not found")
        raise ValueError("Post not found.")
    
    if db_post.author_id != author_id: # If the user is not the author of the post, delete is not allowed
        logging.info(f"User {author_id} is not the author of post {post_id}")
        raise ValueError("Only the post's author can delete it")
    
    delete_stmt = (
        delete(models.Post)
        .where(models.Post.id == post_id)
    )

    db.execute(delete_stmt)
    db.commit()
    return None

def get_post_crud(db: Session, board_id: UUID, post_id: UUID, author_id: UUID) -> Union[models.Post, Tuple[None, str]]:
    board_access = is_board_accessible(db=db, board_id=board_id, user_id=author_id)
    
    if not board_access: # Has no access to the board
        return None, "Board not found or retrieving not allowed"

    stmt = select(models.Post).where(models.Post.id == post_id)
    result = db.execute(stmt)    
    db_post = result.scalars().first()

    if db_post is None:
        return None, "Post not found"
    
        
    return db_post ## If the board is private, only the creator can view it
    
    
def get_post_list_crud(db: Session, board_id: UUID, user_id: UUID, page_number: int, page_size: int) -> Union[schemas.PostList, Tuple[None, str]]:
    board_access = is_board_accessible(db=db, board_id=board_id, user_id=user_id)
    
    if not board_access: # Has no access to the board
        return None, "Board not found or retrieving not allowed"
    
    try:
        offset = (page_number - 1) * page_size # Calculate the offset
        
         # Using select statement
        posts_stmt = (
            select(models.Post)
            .where(models.Post.board_id == board_id)
            .order_by(desc(models.Post.created_at))  # Ordering by created_at in descending order, fetching the latest posts first
            .offset(offset)
            .limit(page_size)
        )     

        posts = db.execute(posts_stmt).scalars().all()
        post_list = [schemas.PostGet(**post.__dict__) for post in posts]

        total_posts_stmt = select(func.count(models.Post.id)).where(models.Post.board_id == board_id)
        total_posts = db.execute(total_posts_stmt).scalar_one()

        
        return schemas.PostList(
            posts=post_list,
            pagination=schemas.Pagination(
                page_number=page_number,
                page_size=page_size,
                total_posts=total_posts,
                total_pages=(total_posts + page_size - 1) // page_size
            )
        )
    except Exception as e:
        logging.exception('An exception occurred while retrieving posts: %s', e)
        return None, "Failed to retrieve posts"



def is_board_accessible(db: Session, board_id: UUID, user_id: UUID) -> bool: # Check if board is public or user is the creator
    # Query the Board database to find the board
    stmt = select(board_models.Board).where(board_models.Board.id == board_id)
    result = db.execute(stmt)    
    db_board = result.scalars().first()

    if db_board is None:
        logging.info(f"Board {board_id} not found")
        return False
    
    if db_board.public: ## If the board is public, anyone can view it
        return True
    
    if db_board.creator == user_id: ## If the user is the creator of the board, they can view it
        return True        
        
    return False # If the board is not public and the user is not the creator, they cannot view it
        