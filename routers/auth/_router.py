from uuid import UUID

from fastapi import APIRouter, status, Form

from routers.tags import Tags

router = APIRouter(
    prefix="/auth",
    tags=[Tags.user, Tags.auth],
    responses={status.HTTP_404_NOT_FOUND: {"message": "Not Found"}},
)


# LOGIN
@router.post("/login")
async def login(username: str = Form(), password: str = Form()):
    # TODO: first, read the security parts
    # 1. we'll use jwt => add header for this
    # 2. return response will be fastapi's redirect response
    # 3. add return type annotations
    raise NotImplementedError()


# LOGOUT
@router.post("/logout/{id}")
async def logout(id: UUID):
    raise NotImplementedError()
