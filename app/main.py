from fastapi import FastAPI
from .auth import router as auth_router
from .movies import router as movies_router
from .admin_movies import router as admin_router

app = FastAPI(title="Cinema API")

app.include_router(auth_router)
app.include_router(movies_router)
app.include_router(admin_router)