from typing import final
from common.utils.password import hash_password


@final
class SignUpService:
    def __init__(self):
        ...

    def _hash_password(self, *, password: str) -> str:
        return hash_password(password=password)


@final
class SignOutService:
    def __init__(self):
        ...


@final
class UpdateAccountService:
    def __init__(self):
        ...
