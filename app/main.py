from fastapi import FastAPI

from . import auth, movies, admin_movies, cart, interactions
from app.database import engine, Base
import app.models

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Cinema API")

app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(admin_movies.router)
app.include_router(cart.router)
app.include_router(interactions.router)