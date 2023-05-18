from typing import Annotated, final
from uuid import UUID

from fastapi import HTTPException, status as HTTPStatus, Depends
from fastapi.security import OAuth2PasswordBearer

from techlog_article.common.config import auth_config
from techlog_article.common.utils.datetime import get_now_timestamp
from techlog_article.common.utils.jwt import (
    create_token as create_jwt_token,
    JWTToken,
    JWTError,
    decode_token as decode_jwt_token,
)
from techlog_article.common.utils.password import verify_password
from techlog_article.common.database.utils import transactional

from .port.in_ import LoginDTO, LoginPort, LogoutPort
from .port.out import ReadUserPort, UpdateAuthDTO, UpdateAuthPort, ReadAuthPort

from ..adapter.out.persistences import UserPersistenceAdapter, AuthPersistenceAdapter


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def _get_credentials_exception(message: str) -> HTTPException:
    return HTTPException(
        status_code=HTTPStatus.HTTP_401_UNAUTHORIZED,
        detail=message,
        headers={"WWW-Authenticate": "Bearer"},
    )


def _decode_token(*, token: str) -> dict[str, str]:
    return decode_jwt_token(token)


async def check_auth_token(
    *,
    token: Annotated[str, Depends(oauth2_scheme)],
    read_auth_port: Annotated[ReadAuthPort, Depends(AuthPersistenceAdapter)],
) -> UUID:
    try:
        payload = _decode_token(token=token)

        # check the user's id
        user_id = payload.get("sub")

        # invalid case 1: invalid token
        if not user_id:
            raise _get_credentials_exception("Could not validate credentials")

        user_id = UUID(user_id)

        # invalid case 2: expired token
        expired_at = int(payload.get("exp"))
        if expired_at < get_now_timestamp():
            raise _get_credentials_exception("The token has expired")
        """
        Remark: The parts involving the DB will be available after
        adding the Redis cache layer afterward
        """
        # auth_in_db = await self._read_auth_port.read_auth_by_user_id(
        #     user_id=user_id
        # )

        # invalid case 3: the user not is not in the DB or deleted
        # if not auth_in_db or auth_in_db.deleted_at:
        #     raise self.get_credentials_exception("The user doesn't exist anymore")

        # invalid case 4: the token is stale(the user logged out before)
        # if not auth_in_db.access_token:
        #     raise self.get_credentials_exception(
        #         "The token is stale: the user must re-login"
        #     )

        return user_id

    except (JWTError, ValueError):
        raise _get_credentials_exception("Token error: Could not validate credentials")


CurrentUserIdDependency = Annotated[UUID, Depends(check_auth_token)]


@final
class LoginService(LoginPort):
    def __init__(
        self,
        *,
        read_user_port: Annotated[ReadUserPort, Depends(UserPersistenceAdapter)],
        update_auth_port: Annotated[UpdateAuthPort, Depends(AuthPersistenceAdapter)],
    ):
        self._read_user_port = read_user_port
        self._update_auth_port = update_auth_port

    @transactional
    async def login(self, *, login_dto: LoginDTO) -> JWTToken:
        user_in_db = await self._read_user_port.read_user_by_name(
            username=login_dto.username
        )
        if not user_in_db:
            raise HTTPException(
                status_code=HTTPStatus.HTTP_404_NOT_FOUND,
                detail=f"User with username {login_dto.username}\
                     doesn't exist in the DB",
                headers={"WWW-authenticate": "Bearer"},
            )

        self._verify_password(
            password=login_dto.password, hashed_password=user_in_db.hashed_password
        )
        token_payload = self._issue_access_token(
            user_id=user_in_db.id,
            is_admin=user_in_db.username == auth_config.ADMIN_USERNAME,
        )

        await self._update_auth_port.update_auth(
            user_id=user_in_db.id,
            dto=UpdateAuthDTO(access_token=token_payload.access_token),
        )

        return token_payload

    def _verify_password(self, *, password: str, hashed_password: str) -> None:
        if not verify_password(password=password, hashed_password=hashed_password):
            raise HTTPException(
                status_code=HTTPStatus.HTTP_400_BAD_REQUEST,
                detail="The provided password doesn't match with the current password",
            )

    def _issue_access_token(self, *, user_id: UUID, is_admin: bool = False) -> JWTToken:
        return create_jwt_token(
            user_id=user_id,
            expiry=get_now_timestamp() + auth_config.ACCESS_TOKEN_EXPRIRES_IN,
            is_admin=is_admin,
        )


@final
class LogoutService(LogoutPort):
    def __init__(
        self,
        *,
        update_auth_port: Annotated[UpdateAuthPort, Depends(AuthPersistenceAdapter)],
    ):
        self._update_auth_port = update_auth_port

    @transactional
    async def logout(self, *, user_id: UUID) -> None:
        await self._update_auth_port.update_auth(
            user_id=user_id, dto=UpdateAuthDTO(access_token=None)
        )
        return None
