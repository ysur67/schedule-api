from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from core.dependencies import DatabaseContextManager, get_db
from modules.lessons_parser.http.base import RequestType
from modules.lessons_parser.http.groups_parser import AllGroupsParser

app = FastAPI()


@app.get("/")
async def index(db: Session = Depends(get_db)):
    return {"message": "hello"}
