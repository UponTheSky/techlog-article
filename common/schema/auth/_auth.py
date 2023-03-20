from uuid import UUID

from pydantic import BaseModel


class UserAuth(BaseModel):
    user_id: UUID
    password: str
