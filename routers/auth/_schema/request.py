from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {"example": {"email": "test@test.com", "password": "1Q2w3e4r!"}}


# TODO: add this part after reading the security parts
class LogoutRequest(BaseModel):
    pass
