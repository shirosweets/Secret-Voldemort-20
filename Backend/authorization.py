from fastapi import HTTPException, status, Depends
from typing import Optional
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from models import TokenData

import db_functions as dbf
import models as md

SECRET_KEY = "5becea4926a7daf6c72854463b1f0a27c400c81fe5ff28baf133af11642d1c88"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120


pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"Authorization": "Bearer"}
    )
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms = [ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email = email)
    except JWTError:
        raise credentials_exception
    user = dbf.get_user_by_email(token_data.email)
    if user is None:
        raise credentials_exception
    return user


def get_user_from_token(token: str):
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms = [ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        token_data = TokenData(email = email)
    except JWTError:
        return None
    user = dbf.get_user_by_email(token_data.email)
    return user


def raise_exception(
        st_code: str,
        message: str,
        head: md.Optional[dict] = None):
    if head is None:
        raise HTTPException(st_code, message)
    else:
        raise HTTPException(st_code, message, head)

async def get_current_active_user(current_user = Depends(get_current_user)):
    if current_user.user_disabled:
        raise_exception(status.HTTP_400_BAD_REQUEST, 'Inactive user')
    return current_user.user_id
