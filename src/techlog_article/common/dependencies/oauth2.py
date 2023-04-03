from typing import Annotated, Union
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from lib.config import config
from lib.utils.datetime import get_now_utc_timestamp

from ..schema.user import User, Admin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_credentials_exception(message: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=message,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> Union[User, Admin]:
    try:
        payload = jwt.decode(
            token, config.SECRET_KEY, algorithms=[config.JWT_ENCODE_ALGORITHM]
        )

        # check the user's id
        user_id = UUID(payload.get("sub"))

        # invalid case 1: invalid token
        if not user_id:
            raise get_credentials_exception("Could not validate credentials")

        # invalid case 2: expired token
        expired_at: int = payload.get("exp")
        if expired_at < get_now_utc_timestamp():
            raise get_credentials_exception("The token has expired")

        # TODO: use cache database to check whether this user_id exists in the DB
        from datetime import datetime

        user_in_db = User(
            id=user_id, name="test", email="test@test.com", created_at=datetime.now()
        )  # note that this shouldn't be User basemodel. This is a temporary object

        user = User(**user_in_db.dict())

        # invalid case 3: if the current token is targeting a user not is not in the DB
        if not user or user.deleted_at:
            raise get_credentials_exception("Could not validate credentials")

        # check whether the user is an admin
        is_admin: bool = payload.get("admin")

        return Admin(**user.dict()) if is_admin else user

        # check the expiry date
    except JWTError:
        raise get_credentials_exception("Token error: Could not validate credentials")


CurrentUserDependency = Annotated[User, Depends(get_current_user)]
