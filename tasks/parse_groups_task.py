from asgiref.sync import async_to_sync
from modules.lessons_parser.http.base import RequestType
from modules.lessons_parser.http.groups_parser import GroupsParser
from worker import celery


@celery.task(name="parse_groups")
async def parse_groups() -> None:
    async_to_sync(run_groups_parser)()


async def run_groups_parser() -> None:
    parser = await GroupsParser.build_parser(
        "http://inet.ibi.spb.ru/raspisan/menu.php?tmenu=1",
        payload_data={},
        request_type=RequestType.GET
    )
    parser.parse()

celery.conf.beat_schedule.update({
    'parse-groups-every-day': {
        'task': 'tasks.parse_groups',
        'schedule': 360,
    },
})
