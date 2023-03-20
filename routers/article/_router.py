from uuid import UUID

from fastapi import APIRouter, Query, Path, Body, status

from common.consts import MAX_ARTICLE_LIMIT
from common.dependencies.oauth2 import CurrentUserDependency

from ._schema.request import CreateArticle, UpdateArticle
from ._schema.response import ArticleResponse

from routers.tags import Tags

# TODO: add dependencies
router = APIRouter(
    prefix="/article",
    tags=[Tags.article],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not Found"}},
)


# READ
@router.get("/", status_code=status.HTTP_200_OK)
async def read_articles(
    offset: int = Query(default=0, ge=0, description="offset for pagination"),
    limit: int = Query(
        default=MAX_ARTICLE_LIMIT, ge=0, description="limit for pagination"
    ),
) -> list[ArticleResponse]:
    raise NotImplementedError()


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def read_article_by_id(id: UUID = Path(...)) -> ArticleResponse:
    raise NotImplementedError()


# CREATE
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_article(
    user: CurrentUserDependency,
    article: CreateArticle = Body(
        description="data required for creating an article item"
    ),
) -> ArticleResponse:
    raise NotImplementedError()


# UPDATE
@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_article(
    *,
    id: UUID = Path(),
    user: CurrentUserDependency,
    data: UpdateArticle = Body(
        description="data required for updating an article item"
    ),
) -> ArticleResponse:
    raise NotImplementedError()


# DELETE
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_article(
    *,
    id: UUID = Path(),
    user: CurrentUserDependency,
) -> ArticleResponse:
    raise NotImplementedError()
