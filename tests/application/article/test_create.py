from unittest import mock
from uuid import uuid4

import pytest

from . import (
    CreateArticleService,
    CreateArticleOutPort,
    CreateArticleInDTO,
    CreateArticleOutDTO,
)


@pytest.fixture
def service() -> CreateArticleService:
    return CreateArticleService(
        create_article_out_port=mock.AsyncMock(spec=CreateArticleOutPort)
    )


@pytest.mark.asyncio
async def test_passes_all_dto_fields(service: CreateArticleService):
    kwargs = {"title": "1", "content": None, "author_id": uuid4()}
    in_dto = CreateArticleInDTO(**kwargs)

    with mock.patch.object(
        CreateArticleOutDTO, "__init__", return_value=None
    ) as mock_constructor:
        await service.create_article(dto=in_dto)
        mock_constructor.assert_called_once_with(**kwargs)
