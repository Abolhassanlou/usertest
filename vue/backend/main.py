from fastapi import FastAPI, Depends, HTTPException , Request , Response
from sqlalchemy.orm import Session
import models, schemas, security ,database

from models import User
from database import engine, get_db
from repositoryuser import SendEmailVerify
import jwt 
from fastapi import BackgroundTasks
models.Base.metadata.create_all(bind=engine)
from security import SECRET_KEY , ALGORITHM , verify_password ,create_access_token
from fastapi import APIRouter
from security import get_current_user

app = FastAPI()

@app.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Check if username or email already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = security.get_password_hash(user.password)
    
    # Create the user (active = False by default)
    db_user = models.User(username=user.username, email=user.email, password=hashed_password, is_active=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Generate the verification token
    token = security.create_verification_token({"username": db_user.username})
    
    # Send the verification email with the token
    background_tasks.add_task(SendEmailVerify.sendVerify, token)  # token = security.create_verification_token({"username": db_user.username})
    
    return db_user

@app.get("/user/verify/{token}")
def verify_user(token: str, db: Session = Depends(get_db)):
    try:
        # Decode the token to get the username
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        
        if username is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        
        # Find the user in the database
        db_user = db.query(models.User).filter(models.User.username == username).first()
        
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if the user is already active
        if db_user.is_active:
            raise HTTPException(status_code=400, detail="User is already active")
        
        # Activate the user
        db_user.is_active = True
        db.commit()
        
        return {"message": "User activated successfully"}
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")


@app.post("/login")
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    # Query for the user using email instead of username
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    # Check if user exists
    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Verify the password
    if not security.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Create an access token
    access_token = security.create_access_token(user=user)

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}!"}

# Optionally, implement a refresh endpoint if needed
@app.post("/refresh")
def refresh_token(request: Request, response: Response):
    # Get the expired token from cookies
    expired_token = request.cookies.get("access_token")
    
    if not expired_token:
        raise HTTPException(status_code=401, detail="Token missing")

    try:
        payload = jwt.decode(expired_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Check if the user exists
        db_user = models.User.query.filter(models.User.email == email).first()
        if db_user is None:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Create new access token
        new_access_token = security.create_access_token(data={"sub": db_user.email})

        
        # Set the new token in cookies
        response.set_cookie(key="access_token", value=new_access_token, httponly=True, secure=True, samesite="Strict")
        return {"message": "Token refreshed"}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

   