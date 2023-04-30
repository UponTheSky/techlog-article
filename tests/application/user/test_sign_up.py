from unittest import mock

import pytest

from . import SignUpService, SignUpDTO, CheckUserPort, CreateUserAuthPort


@pytest.fixture
def service() -> SignUpService:
    return SignUpService(
        check_user_port=mock.Mock(spec=CheckUserPort),
        create_user_auth_port=mock.Mock(spec=CreateUserAuthPort),
    )


@pytest.mark.asyncio
async def test_passes_hashed_password_to_db(service: SignUpService):
    dto = SignUpDTO(
        username="test_test",
        email="test@test.com",
        password="1Q2w3e4r!",
        password_recheck="1Q2w3e4r!",
    )

    with (
        mock.patch.object(service, "_userinfo_exists", return_value=False),
        mock.patch.object(
            service, "_hash_password", return_value="test"
        ) as mock_hasher,
    ):
        await service.sign_up(dto=dto)
        mock_hasher.assert_called_once_with(password=dto.password)
