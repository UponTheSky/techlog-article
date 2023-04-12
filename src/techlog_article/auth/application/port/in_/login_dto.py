from pydantic import BaseModel, Field


class LoginDTO(BaseModel):
    username: str = Field(description="username following the OAuth2 specification")
    password: str = Field(description="password following the OAuth2 specification")
