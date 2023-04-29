from unittest import mock

import pytest

from . import LoginService, ReadUserPort, UpdateAuthPort, UpdateAuthDTO


@pytest.fixture
def service() -> LoginService:
    return LoginService(
        read_user_port=mock.Mock(spec=ReadUserPort),
        update_auth_port=mock.Mock(spec=UpdateAuthPort),
    )


@pytest.mark.asyncio
async def test_passes_four_checks(service: LoginService):
    with (
        mock.patch.object(
            service._read_user_port, "read_user_by_name"
        ) as mock_read_user,
        mock.patch.object(service, "_verify_password") as mock_verify_password,
        mock.patch.object(service, "_issue_access_token") as mock_token_issue,
        mock.patch.object(service._update_auth_port, "update_auth") as mock_update_auth,
        mock.patch.object(UpdateAuthDTO, "__init__", return_value=None),
    ):
        await service.login(login_dto=mock.Mock())
        mock_read_user.assert_awaited_once()
        mock_verify_password.assert_called_once()
        mock_token_issue.assert_called_once()
        mock_update_auth.assert_awaited_once()
