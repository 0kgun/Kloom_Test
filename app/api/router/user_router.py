from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from config.database import get_db
from app.service.user_service import UserService
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserListResponse,
    UserUpdate
)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Create a new user."""
    user = await UserService.create_user(db, user_data)
    return UserResponse(data=user)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get a user by ID."""
    user = await UserService.get_user(db, user_id)
    return UserResponse(data=user)

