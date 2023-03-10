from typing import Optional
import re
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, validator, Field


class UserBase(BaseModel):
    name: Optional[str]
    email: Optional[str]


class User(BaseModel):
    id: UUID
    name: str = Field(min_length=1)
    email: str

    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    # TODO: move it to the router schemas
    @validator("email")
    def email_is_valid(cls, v):
        if not re.match(r"^[\w\d\.]+@[\w\d\.]+\.[\w]+$", v):
            raise ValueError("email should be valid")
        return v
