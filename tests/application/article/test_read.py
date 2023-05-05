from unittest import mock
from uuid import uuid4

import pytest

from fastapi import HTTPException, status as HTTPStatus

from . import (
    ReadArticeService,
    ReadArticleOutPort,
    ReadArticleListResponse,
    ReadArticleListInDTO,
)


@pytest.fixture
def service() -> ReadArticeService:
    return ReadArticeService(
        read_article_out_port=mock.AsyncMock(spec=ReadArticleOutPort)
    )


@pytest.mark.asyncio
async def test_rasies_404_when_article_is_not_found(service: ReadArticeService):
    with (
        mock.patch.object(
            service._read_article_out_port,
            "read_article_by_id_with_author",
            return_value=None,
        ),
        pytest.raises(HTTPException) as exc_info,
    ):
        await service.read_article_by_id(uuid4())

    assert exc_info.value.status_code == HTTPStatus.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_call_both_list_and_count_when_reading_list(service: ReadArticeService):
    with (
        mock.patch.object(
            service._read_article_out_port, "read_article_with_author_list"
        ) as mock_read_list,
        mock.patch.object(
            service._read_article_out_port, "get_total_articles_count"
        ) as mock_count,
        mock.patch.object(ReadArticleListResponse, "__init__", return_value=None),
    ):
        await service.read_article_list(dto=ReadArticleListInDTO())
        mock_read_list.assert_awaited_once()
        mock_count.assert_awaited_once()
