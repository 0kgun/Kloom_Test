from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLAlchemyEnum, Text, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class UserRole(str, Enum):
    """User role enum."""
    FRANCHISE = "franchise"  # 프랜차이즈
    AGENT = "agent"         # 부동산
    OWNER = "owner"         # 예비점주

class User(Base):
    """User database model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100))
    phone = Column(String(20))
    role = Column(SQLAlchemyEnum(UserRole), nullable=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    franchise_profile = relationship("FranchiseProfile", back_populates="user", uselist=False)
    agent_profile = relationship("AgentProfile", back_populates="user", uselist=False)
    owner_profile = relationship("OwnerProfile", back_populates="user", uselist=False)

    properties = relationship("Property", back_populates="agent")

    def __repr__(self):
        return f"<User {self.email}>"

class FranchiseProfile(Base):
    """Franchise profile database model."""
    __tablename__ = "franchise_profiles"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    company_name = Column(String(255))
    position = Column(String(100))
    bio = Column(Text)

    # Relationships
    user = relationship("User", back_populates="franchise_profile")

    def __repr__(self):
        return f"<FranchiseProfile {self.company_name}>"

class AgentProfile(Base):
    """Agent profile database model."""
    __tablename__ = "agent_profiles"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    agency_name = Column(String(255))
    license_number = Column(String(100))
    bio = Column(Text)

    # Relationships
    user = relationship("User", back_populates="agent_profile")

    def __repr__(self):
        return f"<AgentProfile {self.agency_name}>"

class OwnerProfile(Base):
    """Owner profile database model."""
    __tablename__ = "owner_profiles"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    interests = Column(Text)

    # Relationships
    user = relationship("User", back_populates="owner_profile")

    def __repr__(self):
        return f"<OwnerProfile {self.user_id}>" 