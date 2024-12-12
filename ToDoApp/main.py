from src.todo.routers import router as user_router
from src.todo.models import Base
from database import engine

from fastapi import FastAPI

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
