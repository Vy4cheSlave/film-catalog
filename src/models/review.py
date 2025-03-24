from sqlmodel import Field, SQLModel, Relationship
from datetime import date
from .movie import Movie

class ReviewBaseOnlyRating(SQLModel):
    rating: int = Field(ge=1, le=5)

class ReviewBase(ReviewBaseOnlyRating):
    text_review: str = ""

class ReviewPublic(ReviewBase):
    id: int
    movie_id: int
    creation_date: date

class Review(ReviewBase, table=True):
    id: int | None = Field(primary_key=True, default=None)
    creation_date: date= Field()

    movie_id: int= Field(foreign_key="movie.id")
    movie: Movie = Relationship(back_populates="reviews") 