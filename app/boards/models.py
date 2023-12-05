from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db import Base

class Board(Base):  # Base is usually declared in your database setup file
    __tablename__ = "boards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    public = Column(Boolean, default=True)
    creator = Column(UUID(as_uuid=True))

    class Config:
        orm_mode = True