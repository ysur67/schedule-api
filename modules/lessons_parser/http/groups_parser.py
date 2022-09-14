from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from core.di.container import Container
from core.repositories.educational_levels_repository import \
    EducationalLevelsRepository
from core.repositories.groups_repository import GroupsRepository
from core.schemas.group import (CreateEducationalLevelSchema,
                                CreateGroupSchema, EducationalLevel, Group)
from dependency_injector.wiring import Provide, inject
from modules.lessons_parser.http.http_base import BaseHttpParser, Counter
from sqlalchemy.orm import Session


class GroupsParser(BaseHttpParser):
    BASE_URL = "http://inet.ibi.spb.ru/raspisan/menu.php"
    logging_name = "All Groups"

    @inject
    def __init__(
        self,
        url: str,
        payload_data: Dict,
        groups_repository: GroupsRepository = Provide[Container.groups_repository],
        levels_repository: EducationalLevelsRepository = Provide[
            Container.educational_levels_repository
        ],
    ) -> None:
        super().__init__(url, payload_data)
        self.level_counter = Counter(name='educational levels')
        self.groups_counter = Counter(name='groups')
        self._groups_repository = groups_repository
        self._levels_repository = levels_repository

    async def parse(self) -> None:
        select = self.soup.find(id="ucstep")
        assert select, "select can't be None"
        for option in select.find_all("option"):
            level = await self.parse_level(option)
            groups = await self.parse_groups(level)
        self.logger.info('Groups created: %d', self.groups_counter.created)
        self.logger.info('Groups updated: %d', self.groups_counter.updated)
        self.logger.info('Educational levels created: %d',
                         self.level_counter.created)
        self.logger.info('Educational levels updated: %d',
                         self.level_counter.updated)

    async def parse_level(self, item: BeautifulSoup) -> EducationalLevel:
        title = self.get_title(item)
        code = item.attrs.get("value", None)
        assert code, "code can't be None"
        level = await self._levels_repository.get_level_by_title(
            title=title
        )
        if level is not None:
            self.level_counter.append_updated()
            return level
        level = await self._levels_repository.create_level(
            level=CreateEducationalLevelSchema(
                title=title,
                code=code,
            )
        )
        self.level_counter.append_created()
        return level

    async def parse_groups(self, level: EducationalLevel) -> List[Group]:
        groups_soup = await self.get_groups_by_request(level)
        result = []
        for group in groups_soup.find_all("option"):
            result.append(await self._update_or_create_group(group, level))
        return result

    async def _update_or_create_group(
        self,
        group_block: BeautifulSoup,
        level: EducationalLevel
    ) -> Group:
        title = self.get_title(group_block)
        group = await self._groups_repository.get_group_by_title(title=title)
        if group is not None:
            self.groups_counter.append_updated()
            return group
        created_group = await self._groups_repository.create_group(
            group=CreateGroupSchema(
                title=title,
                level=level,
            )
        )
        self.groups_counter.append_created()
        return created_group

    async def get_groups_by_request(self, level: EducationalLevel) -> BeautifulSoup:
        url = self.BASE_URL + f"?tmenu={12}&cod={level.code}"
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")
