from sqlmodel import Session, SQLModel, create_engine
from dotenv import load_dotenv
import os
from sqlalchemy import Engine
from typing import Annotated
from fastapi import Depends
from typing import Generator

class SQLEngine(Engine):
    def __init__(self):
        # load_dotenv(dotenv_path=os.path.join(".", ".env"))
        load_dotenv()
        postgres_user: str = os.environ.get("DB_USER")
        postgres_password: str = os.environ.get("DB_PASSWORD")
        postgres_dbhost: str = os.environ.get("DB_HOST")
        # postgres_dbhost: str = os.environ.get("FAST_API_DB_HOST")
        postgres_dbport: str = os.environ.get("DB_PORT")
        postgres_dbname: str = os.environ.get("DB_NAME")
        postgres_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_dbhost}:{postgres_dbport}/{postgres_dbname}"

        # connect_args = {"check_same_thread": False}
        self.engine = create_engine(postgres_url)#, connect_args=connect_args)

    def engine(self):
        return self._engine

    def get_session(self):
        with Session(self.engine) as session:
            yield session

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

engine = SQLEngine()