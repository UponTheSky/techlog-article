from fastapi import status as HTTPStatus


class AuthError(Exception):
    def __init__(self, *, message: str, code: HTTPStatus):
        super.__init__(message)
        self.message = message
        self.code = code
