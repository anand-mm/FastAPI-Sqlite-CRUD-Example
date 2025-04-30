from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db import get_db
from app.users.exception import CustomException
from app.users.models import ExpoLogin
from app.users.schemas import UserCreate, UserResponse
from app.auth.auth import hash_password
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/",response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)) -> UserResponse:
    new_user = ExpoLogin(
        loginid=user.loginid,
        password=hash_password(user.password),
        usertype=user.usertype,
        createdby=user.createdby  # optional: only if provided
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
    
@router.get("/")
async def read_users(db: AsyncSession= Depends(get_db)) -> list[UserResponse]:
    result = await db.execute(select(ExpoLogin))
    logins = result.scalars().all()
    return logins


@router.get("/{id}")
async def read_users(id: int,db: AsyncSession= Depends(get_db),) -> UserResponse:
    if id == 1:
        raise CustomException(name=id)
    result = await db.execute(select(ExpoLogin).where(ExpoLogin.id == id))
    return result.scalar_one_or_none()
    return await db.query(User).filter(User.id==id).first()
