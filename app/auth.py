from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = utils.hash_password(user_data.password)
    new_user = models.User(
        email=user_data.email,
        hashed_password=hashed_pwd,
        group_id=1
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = utils.generate_activation_token(new_user.id)
    utils.send_activation_email(new_user.email, token)

    return {"message": "User created. Check your email for activation link."}


@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    db.query(models.RefreshToken).filter(models.RefreshToken.token == refresh_token).delete()
    db.commit()
    return {"message": "Successfully logged out"}
