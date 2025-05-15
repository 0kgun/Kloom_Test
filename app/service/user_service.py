from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User, FranchiseProfile, AgentProfile, OwnerProfile
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse, Profile
from app.core.exceptions import NotFoundException, UnauthorizedException

class UserService:
    @staticmethod
    async def get_user(db: Session, user_id: int) -> Optional[User]:
        user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
        if not user:
            raise NotFoundException(detail="User not found")
        return user
    
    @staticmethod
    async def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user."""
        db_user = User(
            email=user_data.email,
            password_hash=user_data.password,
            name=user_data.name,
            phone=user_data.phone,
            role=user_data.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

