from jose import JWTError, jwt
from pydantic import BaseModel
from os import environ
from datetime import datetime, timedelta, timezone

from .load_keys import get_private_key, get_public_key

SECRET_KEY = environ.get("secret_key")
ACCESS_TOKEN_ALGORITHM="HS256"

PRIVATE_KEY=get_private_key()
PUBLIC_KEY=get_public_key()
REFRESH_TOKEN_ALGORITHM="RS256"

ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=1)#5)
REFRESH_TOKEN_EXPIRE_MINUTES = timedelta(minutes=60)#60 * 24 * 7)

class LoginToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRE_MINUTES
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ACCESS_TOKEN_ALGORITHM)
    return encoded_jwt

def decode_access_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM])
        user_id: str = payload.get("sub")
        return user_id
    except JWTError:
        return False


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + REFRESH_TOKEN_EXPIRE_MINUTES
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=REFRESH_TOKEN_ALGORITHM)
    return encoded_jwt

def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[REFRESH_TOKEN_ALGORITHM])
        user_id: str = payload.get("sub")
        return user_id
    except JWTError:
        return False
