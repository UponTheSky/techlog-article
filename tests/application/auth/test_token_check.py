from unittest import mock
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException, status as HTTPStatus

from . import AuthTokenCheckService, ReadAuthPort


@pytest.fixture
def service() -> AuthTokenCheckService:
    return AuthTokenCheckService(
        read_auth_port=mock.Mock(spec=ReadAuthPort),
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload", [{}, {"exp": datetime.now(timezone.utc) + timedelta(seconds=100)}]
)
async def test_raises_401_when_token_is_invalid(
    service: AuthTokenCheckService, payload
):
    with (
        mock.patch.object(service, "_decode_token", return_value=payload),
        pytest.raises(HTTPException) as exc_info,
    ):
        await service(token="")

    assert exc_info.value.status_code == HTTPStatus.HTTP_401_UNAUTHORIZED
