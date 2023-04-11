from typing import Annotated, Optional, Union
from uuid import UUID
from datetime import datetime

from fastapi import Depends, status as http_status_code
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from jose import jwt

from common.config import auth_config
from common.utils import get_now_utc_timestamp, ServiceMessage
from common.schema.user import User, UserInDB
from common.schema.auth import JWTToken, JWTPayload


# TODO: move it to common
class AuthError(Exception):
    def __init__(self, *, message: str, code: http_status_code):
        super.__init__(message)
        self.message = message
        self.code = code


class LoginAuthService:
    def __init__(self, *, token_helper: Annotated["JWTTokenHelper", Depends()]):
        # TODO: change "JWTTokenHelper" from a string to an actually imported module
        self._password_context = CryptContext(
            schemes=[auth_config.PASSWORD_HASH_ALGORITHM], deprecated="auto"
        )
        self._token_helper = token_helper

    def login(
        self, *, username: str, password: str
    ) -> ServiceMessage[Union[JWTToken, AuthError]]:
        try:
            user = self._verify_user(username=username, password=password)

            # TODO: define a constant somewhere else of the username of the admin
            ADMIN_USERNAME = "heyya"
            return ServiceMessage(
                title="success",
                message=self._issue_access_token(
                    user_id=user.id, is_admin=user.username == ADMIN_USERNAME
                ),
            )
        except AuthError as error:
            return ServiceMessage(title="error", message=error)

    # TODO: determine whether or not to use OAuth2PasswordRequestForm
    def _verify_user(self, *, username: str, password: str) -> User:
        user_in_db = self._verify_username(username)
        if not user_in_db:
            raise AuthError(
                message=f"User with username {username} doesn't exist in the DB",
                code=http_status_code.HTTP_404_NOT_FOUND,
            )

        if not self._verify_password(
            password=password, hashed_password=user_in_db.hashed_password
        ):
            raise AuthError(
                message="The provided password doesn't match with the current password",
                code=http_status_code.HTTP_400_BAD_REQUEST,
            )

        return User(**(user_in_db.dict()))

    def _verify_username(self, username) -> Optional[User]:
        # TODO: change this part after implementing the persistence adapter
        # fetch the corresponding entity from the DB
        from uuid import uuid4

        user_in_db: UserInDB = UserInDB(
            username="fake_user",
            email="test@test.com",
            created_at=datetime.now(),
            id=uuid4(),
            hashed_password="12345",
        )
        return user_in_db

    def _verify_password(self, *, password: str, hashed_password: str) -> bool:
        return self._password_context.verify(password, hashed_password)

    def _issue_access_token(self, *, user_id: UUID, is_admin: bool = False) -> JWTToken:
        return self._token_helper.create_token(
            user_id=user_id,
            expiry=get_now_utc_timestamp() + auth_config.ACCESS_TOKEN_EXPRIRES_IN,
            is_admin=is_admin,
        )

    # TODO: move to User service part
    def _hash_password(self, *, password: str) -> str:
        return self._password_context.hash(password)


# TODO: move to dependencies
class AccessAuthService:
    def __init__(self, *, token_helper: Annotated["JWTTokenHelper", Depends()]):
        self._token_helper = token_helper

    def authenticate_user_access_token(self):
        ...
        # TODO: cases
        # 1. if the token is invalid
        # 2. if the token is expired
        # 3. if the token is valid => admin? or an ordinary user?


# TODO: SignIn & SignOut => User domain
class LogoutAuthService:
    def __init__(self, *, token_helper: Annotated["JWTTokenHelper", Depends()]):
        self._token_helper = token_helper

    def logout(self, *, user_id: UUID) -> ServiceMessage[Union[None, AuthError]]:
        if not self._token_helper.deactivate_token(user_id=user_id):
            return ServiceMessage(
                title="error",
                message="internel server error: \
                    token deactivation has been unsuccessful",
            )

        return ServiceMessage(title="error", message=None)


# TODO: move to common
class JWTTokenHelper:
    def __init__(self):
        ...

    def create_token(
        self, *, user_id: UUID, expiry: int, is_admin: bool = False
    ) -> JWTToken:
        payload = JWTPayload(
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

    # TODO: implement deactivate_access_token
    # go straight to the DB and delete the token
    def deactivate_token(self, *, user_id: UUID) -> bool:
        ...
