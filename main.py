from datetime import datetime

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from core.dependencies import get_db
from modules.lessons_parser.http.base import RequestType
from modules.lessons_parser.http.groups_parser import GroupsParser
from modules.lessons_parser.http.lessons_parser import LessonsParser
from utils.date_time import to_message_format

app = FastAPI()


@app.get("/")
async def index(db: Session = Depends(get_db)):
    lessons_start_date = datetime.strptime("01.01.2022", "%d.%m.%Y")
    lessons_end_date = datetime.strptime("01.03.2022", "%d.%m.%Y")
    payload = {
        "rtype": "3",
        "ucstep": "1",
        "exam": "0",
        "datafrom": to_message_format(lessons_start_date),
        "dataend": to_message_format(lessons_end_date),
        "formo": "2",
        "formob": "0",
        "prdis": "0"
    }
    parser = await LessonsParser.build_parser(
        "http://inet.ibi.spb.ru/raspisan/rasp.php",
        payload_data=payload,
        db=db,
    )
    await parser.parse()
    return {"message": "hello"}
