from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import models, schemas
from app.utils import auth_utils
from app.database import get_db
from app.models import UserGroupEnum

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = utils.hash_password(user_data.password)

    new_user = models.User(
        email=user_data.email,
        hashed_password=hashed_pwd,
        group_id=1,
        is_active=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_cart = models.Cart(user_id=new_user.id)
    db.add(new_cart)

    token_str = utils.generate_activation_token(new_user.id)
    db_token = models.ActivationToken(
        user_id=new_user.id,
        token=token_str,
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )
    db.add(db_token)
    db.commit()

    utils.send_activation_email(new_user.email, token_str)

    return {"message": "User created. Check logs for activation link."}


@router.get("/activate/{token}")
def activate_user(token: str, db: Session = Depends(get_db)):
    db_token = db.query(models.ActivationToken).filter(models.ActivationToken.token == token).first()

    if not db_token or db_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    db.delete(db_token)
    db.commit()

    return {"message": "Account activated successfully"}


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account not activated")

    access_token = utils.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_moderator(current_user: models.User = Depends(get_current_user)):
    if current_user.group.name not in [UserGroupEnum.MODERATOR, UserGroupEnum.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have enough permissions"
        )
    return current_user


@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    db.query(models.RefreshToken).filter(models.RefreshToken.token == refresh_token).delete()
    db.commit()
    return {"message": "Successfully logged out"}