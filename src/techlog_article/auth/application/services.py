from typing import Annotated
from uuid import UUID

from fastapi import HTTPException, status as HTTPStatus, Depends
from fastapi.security import OAuth2PasswordBearer

from common.config import auth_config
from common.utils.datetime import get_now_utc_timestamp
from common.utils.jwt import (
    create_token as create_jwt_token,
    JWTToken,
    JWTError,
    decode_token as decode_jwt_token,
)
from common.utils.password import verify_password

from .port.in_ import LoginDTO, LoginPort, LogoutPort
from .port.out import ReadUserPort, UpdateAuthDTO, UpdateAuthPort, ReadAuthPort

from adapter.out.persistences import UserPersistenceAdapter, AuthPersistenceAdapter


class AuthTokenCheckService:
    def __init__(
        self,
        *,
        read_auth_port: Annotated[ReadAuthPort, Depends(AuthPersistenceAdapter)],
    ):
        self._read_auth_port = read_auth_port

    async def __call__(
        self,
        token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="auth/login"))],
    ) -> UUID:
        try:
            payload = decode_jwt_token(token)

            # check the user's id
            user_id = UUID(payload.get("sub"))

            # invalid case 1: invalid token
            if not user_id:
                raise self.get_credentials_exception("Could not validate credentials")

            # invalid case 2: expired token
            expired_at = int(payload.get("exp"))
            if expired_at < get_now_utc_timestamp():
                raise self.get_credentials_exception("The token has expired")

            auth_in_db = await self._read_auth_port.read_auth_by_user_id(
                user_id=user_id
            )

            # invalid case 3: the user not is not in the DB or deleted
            if not auth_in_db or auth_in_db.deleted_at:
                raise self.get_credentials_exception("The user doesn't exist anymore")

            # invalid case 4: the token is stale(the user logged out before)
            if not auth_in_db.access_token:
                raise self.get_credentials_exception(
                    "The token is stale: the user must re-login"
                )

            return user_id

        except JWTError:
            raise self.get_credentials_exception(
                "Token error: Could not validate credentials"
            )

    @staticmethod
    def get_credentials_exception(message: str) -> HTTPException:
        return HTTPException(
            status_code=HTTPStatus.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"},
        )


CurrentUserIdDependency = Annotated[UUID, Depends(AuthTokenCheckService())]


class LoginService(LoginPort):
    def __init__(
        self,
        *,
        read_user_port: Annotated[ReadUserPort, Depends(UserPersistenceAdapter)],
        update_auth_port: Annotated[UpdateAuthPort, Depends(AuthPersistenceAdapter)],
    ):
        self._read_user_port = read_user_port
        self._update_auth_port = update_auth_port

    async def login(self, *, login_dto: LoginDTO) -> JWTToken:
        user_in_db = await self._read_user_port.read_user(username=login_dto.username)
        if not user_in_db:
            raise HTTPException(
                status_code=HTTPStatus.HTTP_404_NOT_FOUND,
                detail=f"User with username {login_dto.username}\
                     doesn't exist in the DB",
            )

        self._verify_password(
            password=login_dto.username, hashed_password=user_in_db.hashed_password
        )
        access_token = self._issue_access_token(
            user_id=user_in_db.id,
            is_admin=user_in_db.username == auth_config.ADMIN_USERNAME,
        )

        await self._update_auth_port.update_auth(
            dto=UpdateAuthDTO(user_id=user_in_db.id, access_token=access_token)
        )

        return access_token

    def _verify_password(self, *, password: str, hashed_password: str) -> None:
        if not verify_password(password=password, hashed_password=hashed_password):
            raise HTTPException(
                status_code=HTTPStatus.HTTP_400_BAD_REQUEST,
                detail="The provided password doesn't match with the current password",
            )

    def _issue_access_token(self, *, user_id: UUID, is_admin: bool = False) -> JWTToken:
        return create_jwt_token(
            user_id=user_id,
            expiry=get_now_utc_timestamp() + auth_config.ACCESS_TOKEN_EXPRIRES_IN,
            is_admin=is_admin,
        )


class LogoutService(LogoutPort):
    def __init__(
        self,
        *,
        update_auth_port: Annotated[UpdateAuthPort, Depends(AuthPersistenceAdapter)],
    ):
        self._update_auth_port = update_auth_port

    async def logout(self, *, user_id: UUID) -> None:
        await self._update_auth_port.update_auth(
            dto=UpdateAuthDTO(user_id=user_id, access_token=None)
        )
        return None
