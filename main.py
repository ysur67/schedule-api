import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from core.dependencies import get_db
from routers.group import router as group_router
from routers.teacher import router as teacher_router

app = FastAPI()
app.include_router(
    group_router,
    prefix="/api/v1"
)
app.include_router(
    teacher_router,
    prefix="/api/v1"
)


@app.get("/")
async def index(db: Session = Depends(get_db)):
    return {"message": "hello"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
