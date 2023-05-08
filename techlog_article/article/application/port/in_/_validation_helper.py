def validate_title(*, title: str) -> str:
    if not (1 <= len(title) <= 32):
        raise ValueError("The title must be of length from 1 to 32")

    return title
