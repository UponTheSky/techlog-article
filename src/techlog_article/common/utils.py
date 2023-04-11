from typing import Literal, TypeVar, Generic
from datetime import datetime, timezone

from pydantic.dataclasses import dataclass


def get_now_utc_timestamp() -> int:
    return int(datetime.timestamp(datetime.now(timezone.utc)))


T = TypeVar("T")


@dataclass
class ServiceMessage(Generic[T]):
    title: Literal["success", "error"]
    payload: T
