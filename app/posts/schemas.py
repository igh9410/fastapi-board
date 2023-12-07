from typing import Optional
from pydantic import BaseModel

class Pagination(BaseModel):
    page_number: int
    page_size: int
    total_posts: int
    total_pages: int

class PostCreate(BaseModel):
    title: str
    content: str
    
class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class PostGet(BaseModel):
    title: str
    content: str



class PostList(BaseModel):
    posts: list[PostGet]
    pagination: Pagination

