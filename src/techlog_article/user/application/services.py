from common.utils.password import hash_password


class UserSignUpService:
    def __init__(self):
        ...

    def _hash_password(self, *, password: str) -> str:
        return hash_password(password=password)
