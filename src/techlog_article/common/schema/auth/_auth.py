from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class JWTToken(BaseModel):
    access_token: str
    token_type: Literal["bearer"]


class JWTPayload(BaseModel):
    iss: str = "techlog-article"
    exp: int
    sub: UUID
    admin: bool = False
