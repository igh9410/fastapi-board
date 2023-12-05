from sqlalchemy import select
from sqlalchemy.orm import Session
from .security import get_password_hash
from .models import User
from .schemas import UserCreate


def create_user(db: Session, user: UserCreate):
    db_user = User(
        fullname=user.fullname,
        email=user.email,
        password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    query = select(User).where(User.email == email)
    result = db.execute(query).scalars().first()
    return result



