import uuid
from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db import Base

class Board(Base):  # Base is usually declared in your database setup file
    __tablename__ = "boards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True, nullable=False)
    public = Column(Boolean, default=True)
    creator = Column(UUID(as_uuid=True))

    posts = relationship("Post", back_populates="board")

    class Config:
        orm_mode = True