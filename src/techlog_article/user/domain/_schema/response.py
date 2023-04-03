from uuid import UUID, uuid4
from datetime import datetime

from common.schema.user import UserCore as _UserCore


class UserResponse(_UserCore):
    id: UUID

    class Config:
        schema_extra = {
            "example": {
                "id": str(uuid4()),
                "name": "test_user",
                "email": "test@test.com",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now()),
            }
        }
