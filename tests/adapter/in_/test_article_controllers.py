from typing import Any
from unittest import mock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from fastapi import status as HTTPStatus

from . import (
    app,
    CreateArticleService,
    ReadArticeService,
    UpdateArticeService,
    check_auth_token,
    ReadArticleInPort,
)


@pytest.fixture(scope="module")
def client() -> TestClient:
    app.dependency_overrides.update(
        {
            CreateArticleService: lambda: mock.AsyncMock(),
            ReadArticeService: lambda: mock.AsyncMock(spec=ReadArticleInPort),
            UpdateArticeService: lambda: mock.AsyncMock(),
            check_auth_token: lambda: uuid4(),
        }
    )

    return TestClient(app=app)


@pytest.mark.parametrize(
    "valid_data",
    [
        {
            "title": "test_test",
        },
        {"title": "test_test", "content": "hey"},
    ],
)
def test_creates_article_successfully_when_given_valid_body(
    client: TestClient, valid_data: dict[str, str]
):
    response = client.post(url="/article", json=valid_data)
    assert response.is_success


@pytest.mark.parametrize(
    "invalid_data",
    [
        {},
        {"content": "hey"},
        {"title": ""},
        {
            "title": "this_title_is_too_long_to_handle_\
            by_the_ui_so_that_we_have_to_restrict_its_length_to_32"
        },
    ],
)
def test_creates_article_unsuccessfully_when_given_invalid_body(
    client: TestClient, invalid_data: dict[str, str]
):
    response = client.post(url="/article", json=invalid_data)
    assert response.status_code == HTTPStatus.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.skip(
    reason="not resolved issue: https://github.com/tiangolo/fastapi/discussions/8724"
)
def test_reads_article_list_successfully_when_given_valid_queries(client: TestClient):
    response = client.get(
        url="/article",
        params={
            "offset": 3,
            "limit": 3,
        },
    )
    assert response.is_success


@pytest.mark.skip(
    reason="not resolved issue: https://github.com/tiangolo/fastapi/discussions/8724"
)
@pytest.mark.parametrize(
    "invalid_data", [("offset", -1), ("limit", 0), ("order_by", "access_token")]
)
def test_reads_article_list_unsuccessfully_when_given_invalid_queries(
    client: TestClient, invalid_data: tuple[str, Any]
):
    key, value = invalid_data
    response = client.get(url="/article", params={key: value})
    assert response.status_code == HTTPStatus.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "valid_data",
    [
        {},
        {
            "title": "test_test",
        },
        {"content": "hey"},
        {"title": "test_test", "content": "hey"},
    ],
)
def test_updates_article_successfully_when_given_valid_body(
    client: TestClient, valid_data: dict[str, str]
):
    response = client.patch(
        url=f"/article/{uuid4()}",
        json=valid_data,
        headers={"Authorization": "Bearer test"},
    )
    assert response.is_success


@pytest.mark.parametrize(
    "invalid_data",
    [
        {
            "title": "this_title_is_too_long_to_handle_\
                by_the_ui_so_that_we_have_to_restrict_its_length_to_32"
        }
    ],
)
def test_updates_article_unsuccessfully_when_given_invalid_body(
    client: TestClient, invalid_data: dict[str, str]
):
    response = client.patch(
        url=f"/article/{uuid4()}",
        json=invalid_data,
        headers={"Authorization": "Bearer test"},
    )
    assert response.status_code == HTTPStatus.HTTP_422_UNPROCESSABLE_ENTITY
