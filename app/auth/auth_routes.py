

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.db import get_db
from app.users.User import User
from app.auth.auth import create_access_token, hash_password, verify_password

from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/auth")

# Mock user database (Replace with real DB)
fake_users_db = {
    "admin": {"username": "admin", "password": hash_password("password123")}
}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""
    user = db.query(User).filter(User.username == form_data.username).first()
    
    # user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token({"sub": form_data.username,"role":user.role}, timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}
