from fastapi import FastAPI
from .auth import router as auth_router

app = FastAPI(title="Cinema API")

app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Cinema API"}