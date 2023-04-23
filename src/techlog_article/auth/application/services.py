from typing import Annotated
from uuid import UUID

from fastapi import HTTPException, status as HTTPStatus, Depends

from common.config import auth_config
from common.utils.datetime import get_now_utc_timestamp
from common.utils.jwt import create_token as create_jwt_token, JWTToken
from common.utils.password import verify_password

from .port.in_ import LoginDTO, LoginPort, LogoutPort
from .port.out import ReadUserPort, UpdateAuthDTO, UpdateAuthPort

from adapter.out.persistences import UserPersistenceAdapter, AuthPersistenceAdapter


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


# TODO: move to dependencies
class AccessAuthService:
    def authenticate_user_access_token(self):
        ...
        # TODO: cases
        # 1. if the token is invalid
        # 2. if the token is expired
        # 3. if the token is valid => admin? or an ordinary user?


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
