from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database
from app.routers import auth

router = APIRouter(prefix="/movies/{movie_uuid}", tags=["interactions"])

@router.post("/like")
def like_movie(movie_uuid: str, is_like: bool, db: Session = Depends(database.get_db), current_user = Depends(
    auth.get_current_user)):
    movie = db.query(models.Movie).filter(models.Movie.uuid == movie_uuid).first()
    existing = db.query(models.MovieLike).filter_by(user_id=current_user.id, movie_id=movie.id).first()
    if existing:
        existing.is_like = is_like
    else:
        db.add(models.MovieLike(user_id=current_user.id, movie_id=movie.id, is_like=is_like))
    db.commit()
    return {"status": "success"}

@router.post("/rate")
def rate_movie(movie_uuid: str, rating: int, db: Session = Depends(database.get_db), current_user = Depends(
    auth.get_current_user)):
    if not (1 <= rating <= 10):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 10")
    movie = db.query(models.Movie).filter(models.Movie.uuid == movie_uuid).first()
    existing = db.query(models.MovieRating).filter_by(user_id=current_user.id, movie_id=movie.id).first()
    if existing:
        existing.rating = rating
    else:
        db.add(models.MovieRating(user_id=current_user.id, movie_id=movie.id, rating=rating))
    db.commit()
    return {"status": "success"}

@router.post("/favorite")
def add_to_favorites(movie_uuid: str, db: Session = Depends(database.get_db), current_user = Depends(
    auth.get_current_user)):
    movie = db.query(models.Movie).filter(models.Movie.uuid == movie_uuid).first()
    db.add(models.FavoriteMovie(user_id=current_user.id, movie_id=movie.id))
    db.commit()
    return {"status": "added to favorites"}
