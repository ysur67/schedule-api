from datetime import date

from core.repositories.groups_repository import GroupsRepository
from core.schemas.group import CreateGroupSchema, Group
from core.service.group import (create_group, get_all_groups, get_group_by_id,
                                get_group_by_title, get_groups_by_level_id)
from core.service.lesson import get_groups_by_date
from sqlalchemy.ext.asyncio import AsyncSession


class AlchemyGroupsRepository(GroupsRepository):

    def __init__(self, db: AsyncSession) -> None:
        super().__init__()
        self.db = db

    async def get_group_by_id(self, id: int) -> Group | None:
        return get_group_by_id(db=self.db, id=id)

    async def get_all_groups(self) -> list[Group]:
        return get_all_groups(self.db)

    async def get_groups_by_educational_level_id(
        self,
        level_id: int,
    ) -> list[Group]:
        return get_groups_by_level_id(self.db, level_id)

    async def get_group_by_title(self, title: str) -> Group | None:
        return get_group_by_title(self.db, title)

    async def create_group(self, group: CreateGroupSchema) -> Group:
        return create_group(self.db, group)

    async def get_groups_by_date(self, date_: date) -> list[Group]:
        return get_groups_by_date(self, date_)
