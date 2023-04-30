from unittest import mock

import pytest
from fastapi.testclient import TestClient

from fastapi import FastAPI
from . import router, SignUpService


@pytest.fixture
def client() -> TestClient:
    app = FastAPI()
    app.include_router(router=router)
    return TestClient(app=app)


def test_sign_up_successful(client: TestClient):
    with mock.patch.object(SignUpService, "sign_up") as mock_serivce:
        response = client.post(
            url="/user",
            data={
                "username": "test_test",
                "email": "test@test.com",
                "password": "1Q2w3e4r!",
                "password_recheck": "1Q2w3e4r!",
            },
        )
        print(response)

        mock_serivce.assert_called_once()
