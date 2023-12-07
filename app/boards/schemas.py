from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class Pagination(BaseModel):
    page_number: int
    page_size: int
    total_pages: int

class Board(BaseModel):
    name: str
    public: bool
    creator: UUID

class BoardGet(BaseModel):
    id: UUID
    name: str
    public: bool

class BoardGetWithPostCount(BaseModel):
    id: UUID
    name: str
    public: bool
    post_count: int

class BoardCreate(BaseModel):
    name: str
    public: bool

class BoardUpdate(BaseModel):
    name: Optional[str] = None
    public: Optional[bool] = None
  

class BoardList(BaseModel):
    boards: list[BoardGetWithPostCount]
    pagination: Pagination
