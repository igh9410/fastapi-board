from pydantic import BaseModel

class BoardCreate(BaseModel):
    name: str
    public: bool