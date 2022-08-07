from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from core.dependencies import get_db
from modules.lessons_parser.http.base import RequestType
from modules.lessons_parser.http.groups_parser import GroupsParser

app = FastAPI()


@app.get("/")
async def index(db: Session = Depends(get_db)):
    parser = await GroupsParser.build_parser(
        "http://inet.ibi.spb.ru/raspisan/menu.php?tmenu=1",
        payload_data={},
        request_type=RequestType.GET,
        db=db,
    )
    await parser.parse()
    return {"message": "hello"}
