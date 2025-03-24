from fastapi import APIRouter
from src.models import MovieBase, MoviePublic, MovieUpdate, Movie, ReviewBaseOnlyRating, ReviewBase, ReviewPublic, Review
from typing import Annotated
from fastapi import Depends, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship, func
from src.enviroment import engine 
from datetime import date

router = APIRouter()

SessionDep = Annotated[Session, Depends(engine.get_session)]

@router.post("/movies", response_model=MoviePublic)
async def create_movie_entry(session: SessionDep, input_body: MovieBase):
    input_body.name = input_body.name.strip().lower()

    movie_is_exist = session.query(Movie).filter(
        Movie.name == input_body.name,
        Movie.year_release == input_body.year_release
    ).first()

    if movie_is_exist:
        raise HTTPException(status_code=409, detail=f"Movie with name \"{input_body.name}\" and year of release \"{input_body.year_release}\" already exists.")
    
    movie_db = Movie.model_validate(input_body)
    session.add(movie_db)
    session.commit()
    session.refresh(movie_db)
    return movie_db

@router.get("/movies", response_model=list[MoviePublic])
async def get_all_movies(session: SessionDep):
    movies_db = session.exec(select(Movie)).all()
    return movies_db

@router.get("/movies/{movie_id}", response_model=MoviePublic)
async def get_movie(session: SessionDep, movie_id: int):
    movie_db = session.get(Movie, movie_id)
    if movie_db is None:
        raise HTTPException(status_code=404, detail=f"Movie with id \"{movie_id}\" not found")
    return movie_db

@router.put("/movies/{movie_id}", response_model=MoviePublic)
async def edit_movie_entry(session: SessionDep, movie_id: int, input_body: MovieUpdate):
    input_body.name = input_body.name.strip().lower()

    movie_db = session.get(Movie, movie_id)
    if not movie_db:
        raise HTTPException(status_code=404, detail=f"Movie with id \"{movie_id}\" not found")
    movie_data = input_body.model_dump(exclude_unset=True)
    movie_db.sqlmodel_update(movie_data)
    session.add(movie_db)
    session.commit()
    session.refresh(movie_db)
    return movie_db

@router.delete("/movies/{movie_id}", response_model=MoviePublic)
async def delete_movie_entry(session: SessionDep, movie_id: int):
    movie_db = session.get(Movie, movie_id)
    if not movie_db:
        raise HTTPException(status_code=404, detail=f"Movie with id \"{movie_id}\" not found")
    session.delete(movie_db)
    session.commit()
    return movie_db

@router.post("/movies/{movie_id}/reviews", response_model=ReviewPublic)
async def add_movie_review(session: SessionDep, movie_id: int, input_body: ReviewBase):
    movie_db = session.exec(select(Movie).where(Movie.id == movie_id)).first()
    if not movie_db:
        raise HTTPException(status_code=404, detail=f"Movie with id \"{movie_id}\" not found")

    review_db = Review(
        **input_body.dict(), 
        movie_id=movie_id, 
        creation_date=date.today()
        )

    session.add(review_db)
    session.commit()
    session.refresh(review_db)
    
    average_rating = session.exec(
        select(func.avg(Review.rating)).where(Review.movie_id == movie_id)
    ).first()
    if average_rating is not None:
        review_db.movie.avg_rating = average_rating
        session.add(review_db.movie)
        session.commit()

    return review_db

@router.get("/movies/{movie_id}/reviews", response_model=list[ReviewPublic])
async def get_all_movie_reviews(session: SessionDep, movie_id: int):
    movie_db = session.exec(select(Movie).where(Movie.id == movie_id)).first()
    if not movie_db:
        raise HTTPException(status_code=404, detail=f"Movie with id \"{movie_id}\" not found")

    return movie_db.reviews

@router.post("/movies/{movie_id}/rate", response_model=ReviewPublic)
async def rating_movie(session: SessionDep, movie_id: int, input_body: ReviewBaseOnlyRating):
    movie_db = session.exec(select(Movie).where(Movie.id == movie_id)).first()
    if not movie_db:
        raise HTTPException(status_code=404, detail=f"Movie with id \"{movie_id}\" not found")

    review_db = Review(
        **input_body.dict(), 
        movie_id=movie_id, 
        creation_date=date.today()
        )
        
    session.add(review_db)
    session.commit()
    session.refresh(review_db)

    average_rating = session.exec(
        select(func.avg(Review.rating)).where(Review.movie_id == movie_id)
    ).first()
    if average_rating is not None:
        review_db.movie.avg_rating = average_rating
        session.add(review_db.movie)
        session.commit()

    return review_db