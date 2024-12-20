from fastapi import FastAPI
from src.App.routes import router as user_router

app = FastAPI()
app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
