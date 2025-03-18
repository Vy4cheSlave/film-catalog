from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

from dotenv import load_dotenv

import os


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


load_dotenv(dotenv_path=os.path.join(".", ".env"))
# load_dotenv()
postgres_user: str = os.environ.get("DB_USER")
postgres_password: str = os.environ.get("DB_PASSWORD")
# postgres_dbhost: str = os.environ.get("DB_HOST")
postgres_dbhost: str = os.environ.get("FAST_API_DB_HOST")
postgres_dbport: str = os.environ.get("DB_PORT")
postgres_dbname: str = os.environ.get("DB_NAME")
postgres_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_dbhost}:{postgres_dbport}/{postgres_dbname}"

# connect_args = {"check_same_thread": False}
engine = create_engine(postgres_url)#, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@app.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}