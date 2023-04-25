from abc import ABC, abstractmethod

from pydantic import BaseModel, Field, validator

from ._validation_helpers import (
    validate_username,
    validate_password,
    validate_email,
    match_passwords,
)


class SignUpDTO(BaseModel):
    username: str = Field(description="The user's name(no need to be a real name)")
    email: str = Field(description="The user's email address")
    password: str = Field(description="The user's password required for login")
    password_recheck: str = Field(
        description="This is for making sure that the user doens't \
            make a unrecognizable password"
    )

    @validator("name")
    def username_is_valid(cls, v):
        return validate_username(username=v)

    @validator("email")
    def email_is_valid(cls, v):
        return validate_email(email=v)

    @validator("password")
    def password_is_valid(cls, v):
        return validate_password(password=v)

    @validator("password_recheck")
    def two_passwords_should_match(cls, v, values, **kwargs):
        return match_passwords(target=v, source=values.get("password"))


class SignUpPort(ABC):
    @abstractmethod
    async def sign_up(self, *, dto: SignUpDTO) -> None:
        ...
