from uuid import UUID

from fastapi import APIRouter

router = APIRouter(
    prefix="/article",
)


# READ
@router.get("/")
async def read_articles():
    # TODO: set offset & limit for pagination
    pass


@router.get("/{id}")
async def read_article_by_id(id: UUID):
    pass


# CREATE
@router.post("/")
async def create_article():
    pass


# UPDATE
@router.patch("/{id}")
async def update_article(id: UUID):
    pass


# DELETE
@router.delete("/{id}")
async def delete_article(id: UUID):
    pass
