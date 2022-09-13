

from abc import ABC, abstractmethod
from typing import Optional

from core.schemas.group import CreateEducationalLevelSchema, EducationalLevel


class EducationalLevelsRepository(ABC):

    @abstractmethod
    async def get_level_by_title(self, title: str) -> EducationalLevel | None:
        pass

    @abstractmethod
    async def get_level_by_id(self, id: int) -> EducationalLevel | None:
        pass

    @abstractmethod
    async def get_all_educational_levels(self) -> list[EducationalLevel]:
        pass

    @abstractmethod
    async def create_level(self, level: CreateEducationalLevelSchema) -> EducationalLevel:
        pass
