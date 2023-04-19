from typing import TypeVar
from datetime import datetime, timezone
from enum import Enum

from fastapi import status as HTTPStatus
from pydantic.dataclasses import dataclass


def get_now_utc_timestamp() -> int:
    return int(datetime.timestamp(datetime.now(timezone.utc)))


T = TypeVar("T")


class ServiceMessageTitle(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


@dataclass
class ServiceMessage:
    title: ServiceMessageTitle
    code: HTTPStatus
    payload: T
