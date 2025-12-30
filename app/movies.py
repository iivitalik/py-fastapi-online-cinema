from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from . import models, schemas, database, auth

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/", response_model=List[schemas.MovieList])
def get_movies(
    skip: int = 0,
    limit: int = 10,
    year: Optional[int] = None,
    imdb_min: Optional[float] = None,
    genre: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "name",
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    query = db.query(models.Movie)

    if year:
        query = query.filter(models.Movie.year == year)
    if imdb_min:
        query = query.filter(models.Movie.imdb >= imdb_min)
    if genre:
        query = query.join(models.Movie.genres).filter(models.Genre.name == genre)
    if search:
        search_filter = or_(
            models.Movie.name.icontains(search),
            models.Movie.description.icontains(search),
            models.Movie.stars.any(models.Star.name.icontains(search)),
            models.Movie.directors.any(models.Director.name.icontains(search))
        )
        query = query.filter(search_filter)

    query = query.order_by(getattr(models.Movie, sort_by))
    return query.offset(skip).limit(limit).all()

@router.get("/{movie_uuid}", response_model=schemas.MovieDetail)
def get_movie_detail(
    movie_uuid: str,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    movie = db.query(models.Movie).filter(models.Movie.uuid == movie_uuid).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie