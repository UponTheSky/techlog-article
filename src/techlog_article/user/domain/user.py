from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class User(BaseModel):
    id: UUID
    username: str = Field(
        min_length=8,
        max_length=16,
        description="Username should be a string of 8 ~ 16 characters",
    )
    hashed_password: str = Field(description="Store the hashed value of the password")
    email: str

    deleted_at: Optional[datetime] = Field(
        description="This is for checking whether the user data is deleted(signed out)"
    )
