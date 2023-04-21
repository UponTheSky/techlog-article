from typing import Literal
from uuid import UUID

from jose import jwt
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from ..config import auth_config


class JWTToken(BaseModel):
    access_token: str
    token_type: Literal["bearer"]


class _JWTPayload(BaseModel):
    iss: str = "techlog-article"
    exp: int
    sub: UUID
    admin: bool = False


def create_token(*, user_id: UUID, expiry: int, is_admin: bool = False) -> JWTToken:
    payload = _JWTPayload(
        exp=expiry,
        sub=user_id,
        admin=is_admin,
    )

    return JWTToken(
        access_token=jwt.encode(
            jsonable_encoder(payload),
            auth_config.JWT_SECRET_KEY,
            algorithm=auth_config.JWT_ENCODE_ALGORITHM,
        ),
        token_type="bearer",
    )
