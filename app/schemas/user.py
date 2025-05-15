from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole

class FranchiseProfileBase(BaseModel):
    """Base franchise profile schema."""
    company_name: Optional[str] = None
    position: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class AgentProfileBase(BaseModel):
    """Base agent profile schema."""
    agency_name: Optional[str] = None
    license_number: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class OwnerProfileBase(BaseModel):
    """Base owner profile schema."""
    interests: Optional[str] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    name: Optional[str] = None
    phone: Optional[str] = None
    role: UserRole

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class UserCreate(UserBase):
    """User creation schema."""
    password: str
    # franchise_profile: Optional[FranchiseProfileBase] = None
    # agent_profile: Optional[AgentProfileBase] = None
    # owner_profile: Optional[OwnerProfileBase] = None

class UserUpdate(BaseModel):
    """User update schema."""
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    franchise_profile: Optional[FranchiseProfileBase] = None
    agent_profile: Optional[AgentProfileBase] = None
    owner_profile: Optional[OwnerProfileBase] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class Profile(BaseModel):
    """Combined profile schema."""
    franchise: Optional[FranchiseProfileBase] = None
    agent: Optional[AgentProfileBase] = None
    owner: Optional[OwnerProfileBase] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class User(UserBase):
    """User schema (response)."""
    id: int
    is_deleted: bool
    created_at: datetime
    profile: Optional[Profile] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class UserResponse(BaseModel):
    """API response schema for user operations."""
    data: User
    message: Optional[str] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class UserListResponse(BaseModel):
    """API response schema for multiple users."""
    data: list[User]
    total: int
    message: Optional[str] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True 