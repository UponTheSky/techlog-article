from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class Auth(BaseModel):
    id: UUID
    user_id: UUID
    access_token: Optional[str] = Field(
        description="The token contains its expiry information as well", default=None
    )

    deleted_at: Optional[datetime] = Field(
        description="This is in sync with the User schema", default=None
    )

    model_config = ConfigDict(from_attributes=True)
