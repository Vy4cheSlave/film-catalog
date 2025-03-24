from sqlmodel import Field, SQLModel, Relationship
from datetime import date

class MovieBase(SQLModel):
    name: str
    description: str | None = Field(default=None)
    year_release: int = Field(ge=1895, le=date.today().year)

class MoviePublic(MovieBase):
    id: int
    avg_rating: float | None = Field(ge=1, le=5, default=None)

class MovieUpdate(MovieBase):
    name: str | None = None
    description: str | None = None
    year_release: int | None = None

class Movie(MovieBase, table=True):
    id: int | None = Field(primary_key=True, default=None)
    avg_rating: float | None = Field(ge=1, le=5, default=None)

    reviews: list["Review"] = Relationship(
        back_populates="movie",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
        )