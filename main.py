from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from core.dependencies import get_db

app = FastAPI()


@app.get("/")
async def index(db: Session = Depends(get_db)):
    return {"message": "hello"}
