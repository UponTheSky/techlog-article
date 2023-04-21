from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Auth(BaseModel):
    id: UUID
    user_id: UUID
    access_token: Optional[str] = Field(
        description="The token contains its expiry information as well"
    )

    class Config:
        orm_mode = True
