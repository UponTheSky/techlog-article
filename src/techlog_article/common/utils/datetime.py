from datetime import datetime


def get_now_datetime() -> datetime:
    return datetime.now()


def get_now_timestamp() -> int:
    return int(datetime.timestamp(get_now_datetime()))
