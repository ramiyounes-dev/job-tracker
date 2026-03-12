from fastapi import Depends, HTTPException
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
import os

from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
jwt_algorithm = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def hash_password(password):    
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    return jwt.encode(
        {**data, 
        "exp": 
            datetime.utcnow() + 
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
        SECRET_KEY,
        algorithm=jwt_algorithm)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[jwt_algorithm])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return user
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
