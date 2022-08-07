from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from core.dependencies import get_db
from core.models import EducationalLevel, Group
from core.schemas.group import CreateEducationalLevelSchema, CreateGroupSchema
from core.service.group import (create_educational_level, create_group,
                                get_educational_level_by_title,
                                get_group_by_title)
from fastapi import Depends
from modules.lessons_parser.http.base import BaseHttpParser, Counter
from sqlalchemy.orm import Session


class AllGroupsParser(BaseHttpParser):
    BASE_URL = "http://inet.ibi.spb.ru/raspisan/menu.php"
    logging_name = "All Groups"

    def __init__(self, url: str, payload_data: Dict, db: Session) -> None:
        super().__init__(url, payload_data)
        self.level_counter = Counter(name='educational levels')
        self.groups_counter = Counter(name='groups')
        self.db = db

    def parse(self):
        select = self.soup.find(id="ucstep")
        assert select, "select can't be None"
        for option in select.find_all("option"):
            level = self.parse_level(option)
            groups = self.parse_groups(level)
        self.logger.info('Groups created: %d', self.groups_counter.created)
        self.logger.info('Groups updated: %d', self.groups_counter.updated)
        self.logger.info('Educational levels created: %d',
                         self.level_counter.created)
        self.logger.info('Educational levels updated: %d',
                         self.level_counter.updated)

    def parse_level(self, item: BeautifulSoup) -> EducationalLevel:
        title = self.get_title(item)
        code = item.attrs.get("value", None)
        assert code, "code can't be None"
        level = get_educational_level_by_title(
            db=self.db,
            title=title
        )
        if not level:
            level = create_educational_level(
                db=self.db,
                level=CreateEducationalLevelSchema(
                    title=title,
                    code=code,
                )
            )
            self.level_counter.append_created()
            return level
        self.level_counter.append_updated()
        return level

    def parse_groups(self, level: EducationalLevel) -> List[Group]:
        groups_soup = self.get_groups_by_request(level)
        result = []
        for group in groups_soup.find_all("option"):
            title = self.get_title(group)
            group = get_group_by_title(db=self.db, title=title)
            if not group:
                group = create_group(
                    db=self.db,
                    group=CreateGroupSchema(
                        title=title,
                        level=level,
                    )
                )
                self.groups_counter.append_created()
                result.append(group)
                continue
            self.groups_counter.append_updated()
            result.append(group)
        return result

    def get_groups_by_request(self, level: EducationalLevel) -> BeautifulSoup:
        url = self.BASE_URL + f"?tmenu={12}&cod={level.code}"
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")
