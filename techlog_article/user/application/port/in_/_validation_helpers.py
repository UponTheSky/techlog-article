from typing import Optional
import re


def validate_username(*, username: str) -> str:
    if not re.match(r"[a-z\d\_]+", username):
        raise ValueError(
            "A username must only consist of alphabet \
                lowercases, digits, and underscores"
        )

    if not (8 <= len(username) <= 16):
        raise ValueError("A username must be of length from 8 to 16")

    return username


def validate_password(*, password: str) -> str:
    if not (
        re.match(r"[a-zA-Z\d\!\@\#\$\%\^\&\*\(\)]+", password)
        and re.search(r"[a-z]", password)
        and re.search(r"[A-Z]", password)
        and re.search(r"\d", password)
        and re.search(r"[\!\@\#\$\%\^\&\*\(\)]", password)
        and (8 <= len(password) <= 16)
    ):
        raise ValueError(
            """
    A password must only contain:
        - at least one of alphabet lowercase
        - at least one of alphabet uppercase
        - at least one of digits
        - at least one of those special characters: !@#$%^&*()
    Also, the length should be at least 8 and at most 16
    """
        )
    return password


def validate_email(*, email: str) -> str:
    if not re.match(r"^[a-z\d\.]+@[a-z\d\.]+\.[a-z]+$", email):
        raise ValueError("Your email should be valid")
    return email


def match_passwords(*, target: str, source: Optional[str]) -> bool:
    if target != source:
        raise ValueError("The passwords should be equal")
    return target
