from core.dependencies import get_db
from core.repositories import (ClassroomsRepository,
                               EducationalLevelsRepository, GroupsRepository,
                               LessonsRepository, SubjectsRepository,
                               TeachersRepository)
from data.repositories import (AlchemyClassroomsRepository,
                               AlchemyEducationalLevelsRepository,
                               AlchemyGroupsRepository,
                               AlchemyLessonsRepository,
                               AlchemySubjectsRepository,
                               AlchemyTeachersRepository)
from dependency_injector.containers import (DeclarativeContainer,
                                            WiringConfiguration)
from dependency_injector.providers import Factory, Resource, Singleton
from sqlalchemy.ext.asyncio import AsyncSession


class Container(DeclarativeContainer):
    db_session: Resource[AsyncSession] = Resource(get_db)
    classrooms_repository: Factory[ClassroomsRepository] = Factory(
        AlchemyClassroomsRepository,
        db=db_session
    )
    educational_levels_repository: Factory[EducationalLevelsRepository] = Factory(
        AlchemyEducationalLevelsRepository,
        db=db_session,
    )
    groups_repository: Factory[GroupsRepository] = Factory(
        AlchemyGroupsRepository,
        db=db_session
    )
    lessons_repository: Factory[LessonsRepository] = Factory(
        AlchemyLessonsRepository,
        db=db_session,
    )
    subjects_repository: Factory[SubjectsRepository] = Factory(
        AlchemySubjectsRepository,
        db=db_session
    )
    teachers_repository: Factory[TeachersRepository] = Factory(
        AlchemyTeachersRepository,
        db=db_session,
    )
