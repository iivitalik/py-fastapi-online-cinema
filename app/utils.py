import secrets
from passlib.context import CryptContext
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def generate_activation_token(user_id: int):
    return secrets.token_urlsafe(32)

def send_activation_email(email: str, token: str):
    print(f"Sending email to {email} with token: {token}")
