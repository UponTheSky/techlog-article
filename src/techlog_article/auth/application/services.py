from typing import Annotated, Optional, Union
from uuid import UUID

from fastapi import Depends, status as HTTPStatus
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from jose import jwt

from common.config import auth_config
from common.utils.datetime import get_now_utc_timestamp
from common.utils.message import ServiceMessage
from common.schema.user import User
from common.schema.auth import JWTToken, JWTPayload
from common.exceptions import AuthError

from .port.in_.login import LoginPort, LoginDTO
from .port.in_.logout import LogoutPort
from .port.out.read_user_port import ReadUserPort
from .port.out.update_auth_port import UpdateAuthPort, UpdateAuthDTO


class LoginService(LoginPort):
    def __init__(
        self,
        *,
        read_user_port: ReadUserPort,
        update_auth_port: UpdateAuthPort,
        token_helper: Annotated["JWTTokenHelper", Depends()],
    ):
        # TODO: change "JWTTokenHelper" from a string to an actually imported module
        self._read_user_port = read_user_port
        self._update_auth_port = update_auth_port
        self._password_context = CryptContext(
            schemes=[auth_config.PASSWORD_HASH_ALGORITHM], deprecated="auto"
        )
        self._token_helper = token_helper

    def login(
        self, *, login_dto: LoginDTO
    ) -> ServiceMessage[Union[JWTToken, AuthError]]:
        try:
            user = self._verify_user(
                username=login_dto.username, password=login_dto.password
            )
            # TODO: define a constant somewhere else of the username of the admin
            ADMIN_USERNAME = "heyya"
            access_token = self._issue_access_token(
                user_id=user.id, is_admin=user.username == ADMIN_USERNAME
            )

            self._update_auth_port.update_auth(
                dto=UpdateAuthDTO(user_id=user.id, access_token=access_token)
            )

            return ServiceMessage(
                title="success", code=HTTPStatus.HTTP_200_OK, message=access_token
            )
        except AuthError as error:
            return ServiceMessage(title="error", code=error.code, message=error.message)

    def _verify_user(self, *, username: str, password: str) -> User:
        user = self._read_user_port.read_user(username=username)
        if not user:
            raise AuthError(
                message=f"User with username {username} doesn't exist in the DB",
                code=HTTPStatus.HTTP_404_NOT_FOUND,
            )

        if not self._verify_password(
            password=password, hashed_password=user.hashed_password
        ):
            raise AuthError(
                message="The provided password doesn't match with the current password",
                code=HTTPStatus.HTTP_400_BAD_REQUEST,
            )

        return user

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
class LogoutService(LogoutPort):
    def __init__(self, *, token_helper: Annotated["JWTTokenHelper", Depends()]):
        self._token_helper = token_helper

    def logout(self, *, user_id: UUID) -> ServiceMessage[Optional[AuthError]]:
        if not self._token_helper.deactivate_token(user_id=user_id):
            return ServiceMessage(
                title="error",
                code=HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR,
                message="internel server error: \
                    token deactivation has been unsuccessful",
            )

        return ServiceMessage(
            title="error", code=HTTPStatus.HTTP_204_NO_CONTENT, message=None
        )


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
