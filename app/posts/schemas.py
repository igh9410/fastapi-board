from pydantic import BaseModel, UUID4

class PostCreate(BaseModel):
    title: str
    content: str
    board_id: UUID4
