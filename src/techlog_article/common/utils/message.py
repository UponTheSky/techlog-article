from typing import TypeVar, Generic
from enum import Enum

from fastapi import status as HTTPStatus
from pydantic.dataclasses import dataclass


Payload = TypeVar("Payload")


class ServiceMessageTitle(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


@dataclass
class ServiceMessage(Generic[Payload]):
    title: ServiceMessageTitle
    code: HTTPStatus
    payload: Payload
