from datetime import datetime, timedelta

from asgiref.sync import async_to_sync
from celery import Celery
from core.database import async_session
from core.dependencies import get_db
from modules.lessons_parser.http.lessons_parser import LessonsParser
from utils.date_time import to_message_format


def init_tasks(celery: Celery):

    @celery.task(name="parse_lessons")
    def parse_lessons() -> None:
        async_to_sync(run_lessons_parser)()

    async def run_lessons_parser() -> None:
        now = datetime.now()
        start_date = now - timedelta(days=10)
        end_date = now + timedelta(days=100)
        async with async_session() as db:
            parser = await LessonsParser.build_parser(
                "http://inet.ibi.spb.ru/raspisan/rasp.php",
                payload_data={
                    "rtype": "3",
                    "ucstep": "1",
                    "exam": "0",
                    "datafrom": to_message_format(start_date),
                    "dataend": to_message_format(end_date),
                    "formo": "2",
                    "formob": "0",
                    "prdis": "0"
                },
                db=db,
            )
            await parser.parse()

    celery.conf.beat_schedule.update({
        'parse-lessons-every-three-hours': {
            'task': 'parse_lessons',
            'schedule': 10_800,
        },
    })
