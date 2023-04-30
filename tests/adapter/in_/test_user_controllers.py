from unittest import mock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from fastapi import status as HTTPStatus

from . import (
    app,
    SignUpService,
    UpdateAccountService,
    SignOutService,
    AuthTokenCheckServiceDependency,
)


@pytest.fixture(scope="module")
def client() -> TestClient:
    app.dependency_overrides.update(
        {
            SignUpService: lambda: mock.AsyncMock(),
            UpdateAccountService: lambda: mock.AsyncMock(),
            SignOutService: lambda: mock.AsyncMock(),
            AuthTokenCheckServiceDependency: lambda: uuid4(),
        }
    )

    return TestClient(app=app)


def test_sign_ups_successfully_when_data_is_valid(client: TestClient):
    response = client.post(
        url="/user",
        data={
            "username": "test_test",
            "email": "test@test.com",
            "password": "1Q2w3e4r!",
            "password_recheck": "1Q2w3e4r!",
        },
    )
    assert response.is_success


@pytest.mark.parametrize(
    "invalid_data",
    [
        {
            "username": "test",
            "email": "test@test.com",
            "password": "1Q2w3e4r!",
            "password_recheck": "1Q2w3e4r!",
        },
        {
            "username": "test_test",
            "email": "test@test!.com",
            "password": "1Q2w3e4r!",
            "password_recheck": "1Q2w3e4r!",
        },
        {
            "username": "test_test",
            "email": "test@test.com",
            "password": "1Q2w3e4r",
            "password_recheck": "1Q2w3e4r",
        },
        {
            "username": "test_test",
            "email": "test@test.com",
            "password": "1Q2w3e4r!",
            "password_recheck": "1Q2w3e4r!123",
        },
    ],
)
def test_sign_ups_unsuccessfully_when_data_is_invalid(
    client: TestClient, invalid_data: dict[str, str]
):
    response = client.post(url="/user", data=invalid_data)
    assert response.status_code == HTTPStatus.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "valid_data",
    [
        {
            "email": "test@test.com",
            "password": "1Q2w3e4r!",
            "password_recheck": "1Q2w3e4r!",
        },
        {
            "username": "test_test",
            "password": "1Q2w3e4r!",
            "password_recheck": "1Q2w3e4r!",
        },
        {
            "username": "test_test",
            "email": "test@test.com",
        },
        {},
    ],
)
def test_updates_account_successfully_when_data_is_valid(
    client: TestClient, valid_data: dict[str, str]
):
    response = client.patch(
        url="/user", data=valid_data, headers={"Authorization": "Bearer test"}
    )

    assert response.is_success


@pytest.mark.parametrize(
    "invalid_data",
    [
        {
            "username": "test",
        },
        {
            "email": "test@test!.com",
        },
        {
            "password": "1Q2w3e4r",
            "password_recheck": "1Q2w3e4r",
        },
        {
            "password": "1Q2w3e4r!",
            "password_recheck": "1Q2w3e4r!123",
        },
        {
            "password": "1Q2w3e4r!",
        },
    ],
)
def test_updates_account_unsuccessfully_when_data_is_invalid(
    client: TestClient, invalid_data: dict[str, str]
):
    response = client.patch(
        url="/user", data=invalid_data, headers={"Authorization": "Bearer test"}
    )
    assert response.status_code == HTTPStatus.HTTP_422_UNPROCESSABLE_ENTITY
