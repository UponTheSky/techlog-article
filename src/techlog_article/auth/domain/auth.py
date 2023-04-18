from uuid import UUID

from pydantic import BaseModel


class Auth(BaseModel):
    id: UUID
    user_id: UUID
    access_token: str
