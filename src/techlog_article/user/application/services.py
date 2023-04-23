from typing import final
from common.utils.password import hash_password


@final
class UserSignUpService:
    def __init__(self):
        ...

    def _hash_password(self, *, password: str) -> str:
        return hash_password(password=password)


@final
class UserSignOutService:
    def __init__(self):
        ...


@final
class UserAccountUpdateService:
    def __init__(self):
        ...
