from passlib.context import CryptContext

from ..config import auth_config


password_context = CryptContext(
    schemes=[auth_config.PASSWORD_HASH_ALGORITHM], deprecated="auto"
)


def verify_password(*, password: str, hashed_password: str) -> bool:
    return password_context.verify(secret=password, hash=hashed_password)


def hash_password(password: str) -> str:
    return password_context.hash(password)
