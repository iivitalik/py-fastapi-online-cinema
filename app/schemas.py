from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
import re

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

    @validator("password")
    def password_complexity(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        return v

class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)

class GenreBase(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class MovieList(BaseModel):
    id: int
    uuid: str
    name: str
    year: int
    imdb: float
    price: Decimal
    genres: List[GenreBase]
    class Config:
        from_attributes = True

class MovieDetail(MovieList):
    description: str
    time: int
    votes: int
    meta_score: Optional[float]
    gross: Optional[float]
    certification: GenreBase
    stars: List[GenreBase]
    directors: List[GenreBase]

class MovieBase(BaseModel):
    name: str
    year: int
    time: int
    imdb: float
    votes: int
    description: str
    price: Decimal
    certification_id: int

class MovieCreate(MovieBase):
    pass

class CommentBase(BaseModel):
    text: str
    parent_id: Optional[int] = None

class CommentCreate(CommentBase):
    pass

class CommentOut(CommentBase):
    id: int
    user_id: int
    movie_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class CartItem(BaseModel):
    movie_id: int
    movie_title: str
    class Config:
        from_attributes = True

class CartOut(BaseModel):
    items: List[CartItem]
    total_count: int
    class Config:
        from_attributes = True
