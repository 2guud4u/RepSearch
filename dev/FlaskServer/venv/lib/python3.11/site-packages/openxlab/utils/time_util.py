from datetime import datetime
import pytz


def get_current_formatted_time(timezone='Asia/Shanghai') -> str:
    formatted_date = get_current_time(timezone).strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date


def get_current_time(timezone='Asia/Shanghai') -> datetime:
    now_utc = datetime.now(tz=pytz.utc)
    tz = pytz.timezone(timezone)
    return now_utc.astimezone(tz)


def get_datetime_from_formatted_str(time_str, timezone='Asia/Shanghai') -> datetime:
    if len(time_str) == 0:
        raise ValueError("formatted time string must not be empty")
    timezone = pytz.timezone(timezone)
    return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone)
