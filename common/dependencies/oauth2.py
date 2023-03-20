from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from ..schema.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # TODO: implement decode_token
    # decoded_token = decode_token(token)
    from datetime import datetime
    from uuid import uuid4

    user = User(
        id=uuid4(), name="test", email="test@test.com", created_at=datetime.now()
    )
    return user


CurrentUserDependency = Annotated[User, Depends(get_current_user)]
