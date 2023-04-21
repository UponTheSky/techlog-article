from uuid import UUID

from pydantic import BaseModel


class UpdateAuthDTO(BaseModel):
    user_id: UUID
    access_token: str
