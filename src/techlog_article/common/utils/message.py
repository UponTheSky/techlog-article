from typing import TypeVar
from enum import Enum

from fastapi import status as HTTPStatus
from pydantic.dataclasses import dataclass


T = TypeVar("T")


class ServiceMessageTitle(str, Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


@dataclass
class ServiceMessage:
    title: ServiceMessageTitle
    code: HTTPStatus
    payload: T
