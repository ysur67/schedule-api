from datetime import date, time, timedelta
from functools import singledispatch
from typing import Generator


@singledispatch
def to_message_format(data: date | time) -> str:
    raise NotImplementedError(f"There is no approach for type {type(data)}")


@to_message_format.register(date)
def _(data: date) -> str:
    return data.strftime('%d.%m.%Y')


@to_message_format.register(time)
def _(data: time) -> str:
    return data.strftime("%H:%M")


def date_range(start_date: date, end_date: date) -> Generator[date, None, None]:
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
