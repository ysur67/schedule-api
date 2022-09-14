from core.repositories.educational_levels_repository import \
    EducationalLevelsRepository
from core.schemas.group import CreateEducationalLevelSchema, EducationalLevel
from core.service.group import (create_educational_level,
                                get_all_educational_levels,
                                get_educational_level_by_id,
                                get_educational_level_by_title)
from sqlalchemy.ext.asyncio import AsyncSession


class AlchemyEducationalLevelsRepository(EducationalLevelsRepository):

    def __init__(self, db: AsyncSession) -> None:
        super().__init__()
        self.db = db

    async def get_level_by_title(self, title: str) -> EducationalLevel | None:
        return get_educational_level_by_title(self.db, title)

    async def get_level_by_id(self, id: int) -> EducationalLevel | None:
        return get_educational_level_by_id(self.db, id)

    async def get_all_educational_levels(self) -> list[EducationalLevel]:
        return get_all_educational_levels(self.db)

    async def create_level(self, level: CreateEducationalLevelSchema) -> EducationalLevel:
        return create_educational_level(self.db, level)
