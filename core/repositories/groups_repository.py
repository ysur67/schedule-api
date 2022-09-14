from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from core.schemas.group import CreateGroupSchema, Group


class GroupsRepository(ABC):

    @abstractmethod
    async def get_group_by_id(self, id: int) -> Group | None:
        pass

    @abstractmethod
    async def get_all_groups(self) -> list[Group]:
        pass

    @abstractmethod
    async def get_groups_by_educational_level_id(
        self,
        level_id: int,
    ) -> list[Group]:
        pass

    @abstractmethod
    async def get_group_by_title(self, title: str) -> Group | None:
        pass

    @abstractmethod
    async def create_group(self, group: CreateGroupSchema) -> Group:
        pass

    @abstractmethod
    async def get_groups_by_date(self, date_: date) -> list[Group]:
        pass
