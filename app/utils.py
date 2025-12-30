import secrets
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "your-secret-key-change-me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str):
    return f"hashed_{password}"

def verify_password(plain_password: str, hashed_password: str):
    return hashed_password == f"hashed_{plain_password}"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def generate_activation_token(user_id: int):
    return secrets.token_urlsafe(32)

def send_activation_email(email: str, token: str):
    print(f"Sending email to {email} with token {token}")
