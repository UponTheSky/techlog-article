from uuid import UUID

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: UUID
    username: str
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)
