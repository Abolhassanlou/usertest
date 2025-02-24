from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import APIRouter, Depends, HTTPException, Response, status, Request ,Request
from typing import Dict , Optional
from models import User
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel



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
        return payload.get("sub")  # This should return the email of the user
    except JWTError:
        return None
    
def get_user_from_db(email: str) -> User:
    db = SessionLocal()  # Ensure you have a SessionLocal defined in your database file
    user = db.query(User).filter(User.email == email).first()  # Query the database for the user with the email
    db.close()  # Close the session
    return user

def get_current_user(request: Request, token: str = Depends(oauth2_scheme)) -> User:
    """Get the current user from the token"""
    # Try to get the user from the token in Authorization header
    if token:
        email = verify_token(token)
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        user = get_user_from_db(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    
    # If no token, try to get from cookies
    token_from_cookie = request.cookies.get("access_token")
    if token_from_cookie:
        email = verify_token(token_from_cookie)
        if not email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        user = get_user_from_db(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    
    # If no valid token or cookie is available, raise an error
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No valid authentication method found")

