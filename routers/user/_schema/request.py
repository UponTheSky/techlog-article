from typing import Optional
import re
from uuid import UUID, uuid4

from pydantic import BaseModel, validator, Field


def _validate_username(username: str) -> str:
    if not re.match(r"[a-z\d\_]+", username):
        raise ValueError(
            "A username must only consist of alphabet \
                lowercases, digits, and underscores"
        )
    return username


def _validate_password(password: str) -> str:
    if not (
        re.match(r"[a-zA-Z\d\!\@\#\$\%\^\&\*\(\)]+", password)
        or re.search(r"[a-z]", password)
        or re.search(r"[A-Z]", password)
        or re.search(r"\d", password)
        or re.search(r"[\!\@\#\$\%\^\&\*\(\)]", password)
        or (8 <= len(password) <= 15)
    ):
        raise ValueError(
            """
    A password must only contain:
        - at least one of alphabet lowercase
        - at least one of alphabet uppercase
        - at least one of digits
        - at least one of those special characters: !@#$%^&*()
    Also, the length should be at least 8 and at most 15
    """
        )
    return password


def _match_passwords(target: Optional[str], source: str) -> bool:
    if not target or target != source:
        raise ValueError("The passwords should be equal")
    return target


class CreateUser(BaseModel):
    name: str = Field(description="The user's name(no need to be a real name)")
    email: str = Field(
        description="The user's email address; \
            probably we could add email validation process in the future"
    )
    password: str = Field(description="The user's password required for login")
    password_recheck: str = Field(
        description="This is for making sure that the user doens't \
            make a unrecognizable password"
    )

    @validator("name")
    def username_is_valid(cls, v):
        return _validate_username(v)

    @validator("email")
    def email_is_valid(cls, v):
        if not re.match(r"^[\w\d\.]+@[\w\d\.]+\.[\w]+$", v):
            raise ValueError("Your email should be valid")
        return v

    @validator("password")
    def password_is_valid(cls, v):
        return _validate_password(v)

    @validator("password_recheck")
    def two_passwords_should_match(cls, v, values, **kwargs):
        return _match_passwords(v, values.get("password1"))

    class Cnofig:
        schema_extra = {
            "example": {
                "name": "testname",
                "email": "test@test.com",
                "password": "1Q2w3e4r!",
                "password_recheck": "1Q2w3e4r!",
            }
        }


class ReadUser(BaseModel):
    id: UUID


class UpdateUser(BaseModel):
    id: UUID
    name: Optional[str]
    password: Optional[str]
    password_recheck: Optional[str] = Field(
        description="This should be not null if password1 is to be passed"
    )

    @validator("name")
    def username_is_valid(cls, v):
        return _validate_username(v) if v else None

    @validator("password")
    def password_is_valid(cls, v):
        return _validate_password(v) if v else None

    @validator("password_recheck")
    def two_password_should_match(cls, v, values, **kwargs):
        password1 = values.get("password1")
        return _match_passwords(v, password1) if password1 else None

    class Config:
        schema_extra = {
            "example": {
                "id": str(uuid4()),
                "name": "updated_name",
                "password": "new_password",
                "password_recheck": "new_password",
            }
        }


class DeleteUser(BaseModel):
    id: UUID
