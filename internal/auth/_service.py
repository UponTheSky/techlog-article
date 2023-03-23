from typing import Optional
from uuid import UUID

from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from jose import jwt

from lib.config import config
from lib.utils.datetime import get_now_utc_timestamp
from common.schema.user import User, UserInDB
from common.schema.auth import JWTToken, JWTPayload


class AuthService:
    def __init__(self):
        self._password_context = CryptContext(
            schemes=[config.ALGORITHM], deprecated="auto"
        )

    def authenticate_user(self, form_data: OAuth2PasswordRequestForm) -> Optional[User]:
        # TODO: either return user or None
        # return user: when the user exists & not deleted
        # return None: either not existing in the DB or user.deleted_at is not None
        from datetime import datetime
        from uuid import uuid4

        # Step 1: fetch the corresponding entity from the DB
        user_in_db: UserInDB = UserInDB(
            username="fake_user",
            email="test@test.com",
            created_at=datetime.now(),
            id=uuid4(),
            hashed_password="12345",
        )
        if not user_in_db:
            # TODO: check the number of failing auth(to prevent malicious tries)
            return None

        # Step 2: check whether the hashed value of the password is equal
        # to the value of the entity from the DB
        # TODO: check the number of failing auth(to prevent malicious tries)
        if not self._verify_password(form_data.password, user_in_db.hashed_password):
            return None

        # if yes, then return the user info(except the hashed password)
        return User(**(user_in_db.dict()))

    def create_access_token(self, user_id: UUID, is_admin: bool = False) -> JWTToken:
        payload = JWTPayload(
            exp=get_now_utc_timestamp() + config.ACCESS_TOKEN_EXPRIRES_IN,
            sub=user_id,
            admin=is_admin,
        )

        return JWTToken(
            access_token=jwt.encode(
                jsonable_encoder(payload),
                config.SECRET_KEY,
                algorithm=config.JWT_ENCODE_ALGORITHM,
            ),
            token_type="bearer",
        )

    # TODO: implement deactivate_access_token
    def deactivate_access_token(self, *args, **kwargs):
        ...

    def logout_user(self, id: UUID) -> User:
        # TODO: how to cancel the user's token?
        ...

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return self._password_context.verify(password, hashed_password)

    def _hash_password(self, password: str) -> str:
        return self._password_context.hash(password)
