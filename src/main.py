from fastapi import FastAPI

from .enviroment import engine
from .routes import router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    engine.create_db_and_tables()

app.include_router(router)