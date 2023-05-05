from typing import Any
from unittest import mock
from uuid import uuid4
from datetime import datetime

import pytest

from . import (
    UpdateAccountService,
    CheckUserPort,
    UpdateUserPort,
    UpdateAccountDTO,
    UpdateUserDTO,
    User,
)


@pytest.fixture
def service() -> UpdateAccountService:
    return UpdateAccountService(
        check_user_port=mock.AsyncMock(spec=CheckUserPort),
        update_user_port=mock.AsyncMock(spec=UpdateUserPort),
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "dto_kwargs",
    [
        {},
        {"username": "test_test", "email": "test@test.com"},
        {
            "password": "1Q2w3e4r!",
            "password_recheck": "1Q2w3e4r!",
            "username": "testtesttest",
        },
        {"email": "test@test.com"},
    ],
)
async def test_passes_only_values_set(
    service: UpdateAccountService, dto_kwargs: dict[str, Any]
):
    user_in_db = User(
        username="test_test",
        email="test@test.com",
        hashed_password="123",
        id=uuid4(),
        created_at=datetime.now(),
    )
    update_account_dto = UpdateAccountDTO(**dto_kwargs)
    hashed_password = "test"

    with (
        mock.patch.object(
            service._check_user_port, "check_exists_by_id", return_value=user_in_db
        ),
        mock.patch.object(
            UpdateUserDTO, "__init__", return_value=None
        ) as mock_dto_constructor,
        mock.patch.object(
            service, "_hash_password", return_value=hashed_password
        ) as mock_hasher,
        mock.patch.object(service._update_user_port, "update_user"),
    ):
        await service.update_account(user_id=user_in_db.id, dto=update_account_dto)
        if "password" in dto_kwargs:
            mock_hasher.assert_called_once()
            del dto_kwargs["password"]
            del dto_kwargs["password_recheck"]
            dto_kwargs["hashed_password"] = hashed_password

        else:
            mock_hasher.assert_not_called()

        mock_dto_constructor.assert_called_once_with(**dto_kwargs)
