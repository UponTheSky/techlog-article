from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CreateArticle(BaseModel):
    title: str = Field(
        description="The article's title should be non-empty when created", min_length=1
    )
    content: str = ""
    author_id: UUID = Field(description="The id field of the 'User' class")

    class Config:
        schema_extra = {
            "example": {
                "title": "How to use FastAPI",
                "content": "# TL; DR",
                "author_id": str(uuid4()),
            }
        }


class ReadArticle(BaseModel):
    id: UUID


class UpdateArticle(BaseModel):
    id: UUID
    title: Optional[str]
    content: Optional[str]

    class Config:
        schema_extra = {"example": {"content": "# Update: ...", "id": f"{uuid4()}"}}


class DeleteArticle(BaseModel):
    id: UUID
