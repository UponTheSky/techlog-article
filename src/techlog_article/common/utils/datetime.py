from datetime import datetime, timezone


def get_now_utc_timestamp() -> int:
    return int(datetime.timestamp(datetime.now(timezone.utc)))
