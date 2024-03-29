from typing import Optional
from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel, validator, ConfigDict

from ._validation_helpers import (
    validate_username,
    validate_password,
    validate_email,
    match_passwords,
)


class UpdateAccountDTO(BaseModel):
    """The optional version of SignUpDTO"""

    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    password_recheck: Optional[str] = None

    @validator("username")
    def username_is_valid(cls, v):
        if not v:
            return None

        return validate_username(username=v)

    @validator("email")
    def email_is_valid(cls, v):
        if not v:
            return None

        return validate_email(email=v) if v else None

    @validator("password")
    def password_is_valid(cls, v):
        if not v:
            return None

        return validate_password(password=v) if v else None

    @validator("password_recheck")
    def two_passwords_should_match(cls, v, values, **kwargs):
        source_password = values.get("password")
        if not source_password and not v:
            return None

        return match_passwords(target=v, source=source_password)

    model_config = ConfigDict(from_attributes=True)


class UpdateAccountPort(ABC):
    @abstractmethod
    async def update_account(self, *, user_id: UUID, dto: UpdateAccountDTO) -> None:
        ...
