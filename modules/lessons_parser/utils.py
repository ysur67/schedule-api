import re
from datetime import date, datetime, time
from typing import Optional, Tuple

from bs4 import BeautifulSoup


def get_time_range_from_string(string: str) -> Tuple[time | None, time | None]:
    """Получить временной диапазон из строки.

    Обязательный формат строки, который используется на данный момент
    `hh:mm-hh:mm`.

    Args:
        string (str): Строка с временным промежутком.

    Raises:
        TypeError: Если строка имеет неправильный формат.

    Returns:
        time, time: Диапазон, вида - начало, конец.
    """
    initial = string.split("-")
    if not initial:
        raise TypeError("time range is invalid")
    try:
        start_hour, start_minute = get_hours_and_minutes(initial[0])
    except ValueError:
        return None, None
    try:
        end_hour, end_minute = get_hours_and_minutes(initial[1])
    except ValueError:
        return None, None
    start = time(hour=start_hour, minute=start_minute)
    end = time(hour=end_hour, minute=end_minute)
    return start, end


def get_hours_and_minutes(string: str) -> Tuple[int, int]:
    """Получить часы и минуты из строки.

    Обязательный формат строки - `hh:mm`

    Args:
        string (str): Строка

    Raises:
        TypeError: Если строка имеет неправильный формат.

    Returns:
        int, int: Часы, минуты.
    """
    initial = string.split(":")
    if not initial:
        raise TypeError("time format is invalid")
    hour = int(initial[0])
    minute = int(initial[1])
    return hour, minute


def get_date_from_string(string: str) -> date:
    """Получить дату из строки.

    Обязательный формат строки `dd.mm.YY DayOfWeek`

    Args:
        string (str): Строка

    Raises:
        TypeError: Если строка имеет неправильный формат

    Returns:
        date: Дата
    """
    initial = string.split(" ")
    if not initial or len(initial) < 2:
        raise TypeError("date format is invalid")
    DATE_FORMAT = "%d.%m.%Y"
    return datetime.strptime(initial[0], DATE_FORMAT).date()


def has_selected_attribute(tag: BeautifulSoup) -> bool:
    return tag.has_attr("selected")


def get_url_from_string(value: str) -> Optional[str]:
    values = re.findall(r'(https?://\S+)', value)
    return values[0] if values else None
