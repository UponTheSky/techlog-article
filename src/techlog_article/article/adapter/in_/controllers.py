from typing import Annotated
from uuid import UUID  # noqa: F401

from fastapi import (
    APIRouter,
    Query,  # noqa: F401
    Path,  # noqa: F401
    Body,
    status as HTTPStatus,
    Depends,
)

from common.consts import MAX_ARTICLE_LIMIT  # noqa: F401
from common.tags import Tags
from auth.application.services import CurrentUserIdDependency

from application.services import CreateArticleService

from application.port.in_ import CreateArticleInDTO, CreateArticleInPort

from ._dtos import CreateArticleBody


router = APIRouter(
    prefix="/article",
    tags=[Tags.article],
    responses={HTTPStatus.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
)


# # READ
# @router.get("/", status_code=HTTPStatus.HTTP_200_OK)
# async def read_articles(
#     offset: int = Query(default=0, ge=0, description="offset for pagination"),
#     limit: int = Query(
#         default=MAX_ARTICLE_LIMIT, ge=0, description="limit for pagination"
#     ),
# ) -> list[ArticleResponse]:
#     raise NotImplementedError()


# @router.get("/{id}", status_code=HTTPStatus.HTTP_200_OK)
# async def read_article_by_id(id: UUID = Path(...)) -> ArticleResponse:
#     raise NotImplementedError()


@router.post("/", status_code=HTTPStatus.HTTP_201_CREATED)
async def create_article(
    *,
    author_id: CurrentUserIdDependency,
    body: CreateArticleBody = Body(),
    create_article_service: Annotated[
        CreateArticleInPort, Depends(CreateArticleService)
    ],
) -> None:
    await create_article_service.create_article(
        dto=CreateArticleInDTO(
            title=body.title, content=body.content, author_id=author_id
        )
    )

    return None


# # UPDATE
# @router.patch("/{id}", status_code=HTTPStatus.HTTP_200_OK)
# async def update_article(
#     *,
#     id: UUID = Path(),
#     user: CurrentUserDependency,
#     data: UpdateArticle = Body(
#         description="data required for updating an article item"
#     ),
# ) -> ArticleResponse:
#     raise NotImplementedError()


# # DELETE
# @router.delete("/{id}", status_code=HTTPStatus.HTTP_200_OK)
# async def delete_article(
#     *,
#     id: UUID = Path(),
#     user: CurrentUserDependency,
# ) -> ArticleResponse:
#     raise NotImplementedError()
