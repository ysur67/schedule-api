from datetime import datetime, timedelta

from asgiref.sync import async_to_sync
from modules.lessons_parser.http.lessons_parser import LessonsParser
from utils.date_time import to_message_format
from worker import celery


@celery.task(name="parse_lessons")
def parse_lessons() -> None:
    async_to_sync(run_lessons_parser)()


async def run_lessons_parser() -> None:
    now = datetime.now()

    parser = await LessonsParser.build_parser(
        "http://inet.ibi.spb.ru/raspisan/rasp.php",
        payload_data={
            "rtype": "3",
            "ucstep": "1",
            "exam": "0",
            "datafrom": to_message_format(now),
            "dataend": to_message_format(now + timedelta(days=100)),
            "formo": "2",
            "formob": "0",
            "prdis": "0"
        }
    )
    await parser.parse()

celery.conf.beat_schedule.update({
    'parse-lessons-every-hour': {
        'task': 'tasks.parse_lessons',
        'schedule': 360,
    },
})
