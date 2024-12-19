from src.todo.routers import router as user_router
from src.todo.models import Base
from database import engine
from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from src.todo.service import startup_event

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(user_router)

# @app.on_event("startup")
# async def begin():
#     await startup_event()

@app.on_event('startup')
def init_data():
    scheduler = BackgroundScheduler()
    scheduler.add_job(startup_event, 'interval', seconds=5, misfire_grace_time=10)
    scheduler.start()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
    





