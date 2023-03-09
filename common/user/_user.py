from typing import Optional
import re
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, validator


class User(BaseModel):
    id: UUID
    name: str
    email: str

    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    # TODO: move it to the router schemas
    @validator("name")
    def name_is_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError("user name should be non-empty")
        return v

    # TODO: move it to the router schemas
    @validator("email")
    def email_is_valid(cls, v):
        if not re.match(r"^[\w\d\.]+@[\w\d\.]+\.[\w]+$", v):
            raise ValueError("email should be valid")
        return v
