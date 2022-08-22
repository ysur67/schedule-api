import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from core.dependencies import get_db
from routers.group import router as groups_router
from routers.lesson import router as lessons_router
from routers.teacher import router as teachers_router

app = FastAPI()
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    groups_router,
    prefix="/api/v1"
)
app.include_router(
    teachers_router,
    prefix="/api/v1"
)
app.include_router(
    lessons_router,
    prefix="/api/v1"
)


@app.get("/")
async def index(db: Session = Depends(get_db)):
    return {"message": "hello"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
