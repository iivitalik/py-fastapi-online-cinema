from fastapi import FastAPI

from app.routers import admin_movies, auth, cart, interactions, movies
from app.database import engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Cinema API")

app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(admin_movies.router)
app.include_router(cart.router)
app.include_router(interactions.router)