from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.dependencies import get_db
from schemas.user import UserCreate, UserResponse
from models.user import User
from db.session import SessionLocal
from services.auth import create_user, authenticate_user, create_jwt_token

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    db = SessionLocal()
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db, user)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    token = create_jwt_token(user)
    return {"access_token": token, "token_type": "bearer"}