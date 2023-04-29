from typing import Any
from unittest import mock
from uuid import uuid4
from datetime import datetime

import pytest

from fastapi import HTTPException, status as HTTPStatus

from . import (
    UpdateArticeService,
    UpdateArticleInDTO,
    UpdateArticleOutDTO,
    UpdateArticleOutPort,
    Article,
)


@pytest.fixture
def service() -> UpdateArticeService:
    return UpdateArticeService(
        update_article_out_port=mock.AsyncMock(spec=UpdateArticleOutPort)
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "dto_kwargs",
    [{"content": "hey"}, {"title": "hey"}, {"title": "hey", "content": "hey"}],
)
async def test_update_passes_only_set_values(
    service: UpdateArticeService, dto_kwargs: dict[str, Any]
):
    article_id, author_id = uuid4(), uuid4()
    dto = UpdateArticleInDTO(**dto_kwargs)

    with (
        mock.patch.object(
            service._update_article_out_port,
            "read_article_by_id",
            return_value=Article(
                id=article_id,
                title="test",
                content="test",
                author_id=author_id,
                created_at=datetime.now(),
            ),
        ) as mock_read,
        mock.patch.object(
            UpdateArticleOutDTO, "__init__", return_value=None
        ) as mock_dto_constructor,
    ):
        await service.update_article(
            author_id=author_id, article_id=article_id, dto=dto
        )

        mock_read.assert_awaited_once()
        mock_dto_constructor.assert_called_once_with(**dto_kwargs)


@pytest.mark.asyncio
async def test_only_author_can_update_article(service: UpdateArticeService):
    """
    Remark: the behavior of the delete service also matches
    what this test tries to check
    """
    with (
        mock.patch.object(
            service._update_article_out_port,
            "read_article_by_id",
            return_value=Article(
                id=uuid4(),
                title="test",
                content="test",
                author_id=uuid4(),
                created_at=datetime.now(),
            ),
        ) as mock_read,
        pytest.raises(HTTPException) as exc_info,
    ):
        await service.update_article(
            author_id=uuid4(), article_id=uuid4(), dto=UpdateArticleInDTO()
        )

        mock_read.assert_awaited_once()

    assert exc_info.value.status_code == HTTPStatus.HTTP_403_FORBIDDEN
