from celery.app.task import Task
from modules.lessons_parser.http.base import RequestType
from modules.lessons_parser.http.groups_parser import GroupsParser


class ParseGroupsTask(Task):

    async def run(self, *args, **kwargs):
        parser = await GroupsParser.build_parser(
            "http://inet.ibi.spb.ru/raspisan/menu.php?tmenu=1",
            payload_data={},
            request_type=RequestType.GET
        )
        return await parser.parse()
