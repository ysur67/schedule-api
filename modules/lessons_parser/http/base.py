import enum
from dataclasses import dataclass
from typing import Dict, Optional, Type, TypeVar

import requests
from bs4 import BeautifulSoup

from ..base import BaseParser

T = TypeVar("T", bound="BaseHttpParser")


class RequestType(enum.Enum):
    GET = "get"
    POST = "post"


@dataclass
class Counter:
    name: Optional[str] = None
    updated: int = 0
    created: int = 0

    def append_created(self, amount: int = 1) -> int:
        self.created += amount
        return self.created

    def append_updated(self, amount: int = 1) -> int:
        self.updated += amount
        return self.updated

    def __str__(self) -> str:
        return f"{self.name}\nCreated: {self.created}\nUpdated: {self.updated}."


class BaseHttpParser(BaseParser):
    request_type: RequestType

    @classmethod
    async def build_parser(
        cls: Type[T],
        url: str,
        request_type: RequestType = RequestType.POST,
        payload_data: Dict = {},
        **kwargs,
    ) -> T:
        parser = cls(url, payload_data, **kwargs)
        parser.request_type = request_type
        await parser.set_up()
        return parser

    def __init__(self, url: str, payload_data: Dict) -> None:
        super().__init__(url)
        self.payload_data = payload_data

    async def on_set_up(self):
        if self.request_type == RequestType.POST:
            request = requests.post(self.url, data=self.payload_data)
        elif self.request_type == RequestType.GET:
            request = requests.get(self.url, data=self.payload_data)
        else:
            raise NotImplementedError(
                f"there is no approach for {self.request_type} method")
        if not request.ok:
            raise ValueError("код ответа не находится в промежутке 200-299")
        self.soup = BeautifulSoup(request.text, "html.parser")

    def get_title(self, item: BeautifulSoup, raise_exception: bool = True) -> Optional[str]:
        """Получить текст из блока BeautifulSoup

        Args:
            item (BeautifulSoup): Блок
            raise_exception (bool, optional): Флаг, указывающий на то, что
            необходимо поднимать исключение, если текста внутри блока нет.
            Defaults to True.
        """
        result = item.get_text().strip()
        if result:
            return result
        if raise_exception:
            raise ValueError("bs item has no title inside it")
        return None
