from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.users.User import User
from app.users.UserSchema import UserCreate, UserResponse
from app.auth.auth import hash_password


router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/",response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    new_user = User(username=user.username,password=hash_password(user.password))
    db.add(new_user); db.commit(); db.refresh(new_user)
    return new_user
    
@router.get("/")
def read_users(db: Session= Depends(get_db)) -> list[UserResponse]:
    return db.query(User).all()


@router.get("/{id}")
def read_users(id: int,db: Session= Depends(get_db),) -> UserResponse:
    return db.query(User).filter(User.id==id).first()
