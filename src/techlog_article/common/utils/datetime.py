from datetime import datetime, timezone


def get_now_datetime() -> datetime:
    return datetime.now(timezone.utc)


def get_now_utc_timestamp() -> int:
    return int(datetime.timestamp(get_now_datetime()))
