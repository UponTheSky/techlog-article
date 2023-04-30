from unittest import mock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from . import (
    app,
    SignUpService,
    SignUpPort,
    UpdateAccountPort,
    SignOutPort,
    UpdateAccountService,
    SignOutService,
    CurrentUserIdDependency,
)


@pytest.fixture(scope="module")
def client() -> TestClient:
    def mock_sign_up_service() -> SignUpPort:
        return mock.AsyncMock(spec=SignUpPort)

    def mock_update_account_service() -> UpdateAccountPort:
        return mock.AsyncMock(spec=UpdateAccountPort)

    def mock_sign_out_service() -> SignOutPort:
        return mock.AsyncMock(spec=SignOutPort)

    app.dependency_overrides.update(
        {
            SignUpService: mock_sign_up_service,
            UpdateAccountService: mock_update_account_service,
            SignOutService: mock_sign_out_service,
            CurrentUserIdDependency: lambda x: uuid4(),
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
def test_sign_up_unsuccessfully_when_data_is_invalid(
    client: TestClient, invalid_data: dict[str, str]
):
    response = client.post(url="/user", data=invalid_data)
    assert response.is_client_error


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
    assert response.is_client_error
