from asgiref.sync import async_to_sync
from celery import Celery
from core.database import async_session
from core.dependencies import get_db
from modules.lessons_parser.http.groups_parser import GroupsParser
from modules.lessons_parser.http.http_base import RequestType


def init_tasks(celery: Celery) -> None:

    @celery.task(name="parse_groups")
    def parse_groups() -> None:
        async_to_sync(run_groups_parser)()

    async def run_groups_parser() -> None:
        async with async_session() as db:
            parser = await GroupsParser.build_parser(
                "http://inet.ibi.spb.ru/raspisan/menu.php?tmenu=1",
                payload_data={},
                request_type=RequestType.GET,
                db=db,
            )
            await parser.parse()

    celery.conf.beat_schedule.update({
        'parse-groups-every-day': {
            'task': 'parse_groups',
            'schedule': 86_400,
        },
    })
