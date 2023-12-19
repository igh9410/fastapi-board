from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)

    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    board_id = Column(UUID(as_uuid=True), ForeignKey("boards.id", ondelete="CASCADE"))
    board = relationship("Board", back_populates="posts")

    class Config:
        orm_mode = True
