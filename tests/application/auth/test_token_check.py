from unittest import mock
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException, status as HTTPStatus

from . import services


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload", [{}, {"exp": datetime.now(timezone.utc) + timedelta(seconds=100)}]
)
async def test_raises_401_when_token_is_invalid(payload: dict):
    with (
        mock.patch.object(services, "_decode_token", return_value=payload),
        pytest.raises(HTTPException) as exc_info,
    ):
        await services.check_auth_token(token="", read_auth_port=mock.Mock())

    assert exc_info.value.status_code == HTTPStatus.HTTP_401_UNAUTHORIZED
