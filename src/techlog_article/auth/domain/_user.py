from pydantic import BaseModel
from uuid import UUID


class User(BaseModel):
    id: UUID
    username: str
    hashed_password: str
