from uuid import UUID
from pydantic import BaseModel

class Board(BaseModel):
    name: str
    public: bool
    creator: UUID

class BoardGet(BaseModel):
    name: str
    public: bool   
   

class BoardCreate(BaseModel):
    name: str
    public: bool

class BoardUpdate(BaseModel):
    name: str
    public: bool

class BoardList(BaseModel):
    boards: list[BoardGet]
