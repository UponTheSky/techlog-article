from typing import Optional
from abc import ABC, abstractmethod

from pydantic import BaseModel, validator

from ._validation_helpers import (
    validate_username,
    validate_password,
    validate_email,
    match_passwords,
)


class UpdateAccountDTO(BaseModel):
    """The optional version of SignUpDTO"""

    name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    password_recheck: Optional[str]

    @validator("name")
    def username_is_valid(cls, v):
        return validate_username(username=v) if v else None

    @validator("email")
    def email_is_valid(cls, v):
        return validate_email(email=v) if v else None

    @validator("password")
    def password_is_valid(cls, v):
        return validate_password(password=v) if v else None

    @validator("password_recheck")
    def two_passwords_should_match(cls, v, values, **kwargs):
        source_password = values.get("password")
        if not source_password and not v:
            return None

        return match_passwords(target=v, source=source_password)

    class Config:
        description = "An optional version of SignUpDTO"


class UpdateAccountPort(ABC):
    @abstractmethod
    async def sign_up(self, *, dto: UpdateAccountDTO) -> None:
        ...
