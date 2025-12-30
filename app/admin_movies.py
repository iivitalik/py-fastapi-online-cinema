from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, database, auth

router = APIRouter(prefix="/admin/movies", tags=["admin-movies"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_movie(
        movie_in: schemas.MovieCreate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_moderator)
):
    new_movie = models.Movie(**movie_in.dict(exclude={"genre_ids", "star_ids", "director_ids"}))

    if movie_in.genre_ids:
        new_movie.genres = db.query(models.Genre).filter(models.Genre.id.in_(movie_in.genre_ids)).all()
    if movie_in.star_ids:
        new_movie.stars = db.query(models.Star).filter(models.Star.id.in_(movie_in.star_ids)).all()
    if movie_in.director_ids:
        new_movie.directors = db.query(models.Director).filter(models.Director.id.in_(movie_in.director_ids)).all()

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie


@router.delete("/{movie_id}")
def delete_movie(
        movie_id: int,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(auth.get_current_moderator)
):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    db.delete(movie)
    db.commit()
    return {"message": "Movie deleted"}
