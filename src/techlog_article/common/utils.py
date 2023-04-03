from datetime import datetime, timezone


def get_now_utc_timestamp() -> datetime:
    return datetime.now(timezone.utc)
