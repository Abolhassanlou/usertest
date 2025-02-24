from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
import jwt
from typing import Dict
from typing import Optional
from models import User
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from database import SessionLocal
from models import User

SECRET_KEY = "mysecret"  # Change this in .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user):
    expire = datetime.utcnow() + timedelta(hours=1)
    return jwt.encode({"sub": user.email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

def create_verification_token(data: Dict):
    expiration = datetime.utcnow() + timedelta(hours=24)  # Token expires in 24 hours
    to_encode = {"exp": expiration, **data}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Update the token URL to match your login route
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_token(token: str):
    """Decode JWT token and return email (sub)"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")  # Returns email
    except JWTError:
        return None

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # or whatever token URL you're using

# Your existing function that fetches the user by email
def get_user_from_db(email: str) -> User:
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()
    return user

# Combined function for token or cookie
def get_current_user(request: Request, token: str = Depends(oauth2_scheme)) -> User:
    # Try to get the user from the token first
    if token:
        email = verify_token(token)
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        user = get_user_from_db(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    
    # Fallback: if no token, try to get the user from the cookie
    token_from_cookie = request.cookies.get("access_token")
    if token_from_cookie:
        email = verify_token(token_from_cookie)
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        user = get_user_from_db(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    
    # If neither token nor cookie is available
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No valid authentication method found")
