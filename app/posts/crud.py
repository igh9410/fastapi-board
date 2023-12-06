from pydantic import UUID4
from sqlalchemy.orm import Session
from . import models, schemas

def create_post_crud(db: Session, post: schemas.PostCreate, author_id: UUID4):
    db_post = models.Post(title=post.title, content=post.content, author_id=author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post