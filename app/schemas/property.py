from sqlalchemy import Boolean, Column, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

# from app.db.base import Base
# from app.models.property import PropertyStatus, PropertyType

from typing import Optional, List
from datetime import date
from pydantic import BaseModel, conint, confloat


class PropertyBase(BaseModel):
    """Base property schema."""
    title: str
    address: str
    region_code: Optional[str] = None
    area_m2: Optional[float] = None
    area_pyeong: Optional[float] = None
    deposit: Optional[int] = None
    monthly_rent: Optional[int] = None
    sale_price: Optional[int] = None
    management_fee: Optional[int] = None
    floor: Optional[int] = None
    building_type: Optional[str] = None
    year_built: Optional[int] = None
    renovated: Optional[bool] = False
    available_from: Optional[date] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PropertyCreate(PropertyBase):
    """Property creation schema."""
    pass


class PropertyUpdate(BaseModel):
    """Property update schema."""
    title: Optional[str] = None
    address: Optional[str] = None
    region_code: Optional[str] = None
    area_m2: Optional[float] = None
    area_pyeong: Optional[float] = None
    deposit: Optional[int] = None
    monthly_rent: Optional[int] = None
    sale_price: Optional[int] = None
    management_fee: Optional[int] = None
    floor: Optional[int] = None
    building_type: Optional[str] = None
    year_built: Optional[int] = None
    renovated: Optional[bool] = None
    available_from: Optional[date] = None
    status: Optional[PropertyStatus] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PropertyDetail(PropertyBase):
    """Property detail schema."""
    id: int
    status: PropertyStatus
    is_deleted: bool
    agent_id: int
    created_at: date
    agent_name: Optional[str] = None
    agent_phone: Optional[str] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class Property(PropertyBase):
    """Property schema."""
    id: int
    status: PropertyStatus
    is_deleted: bool
    agent_id: int
    created_at: date

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class RequestPreferenceBase(BaseModel):
    """Base request preference schema."""
    property_type: Optional[str] = None
    transaction_type: Optional[str] = None
    category: Optional[str] = None
    min_area: Optional[float] = None
    max_area: Optional[float] = None
    min_floor: Optional[int] = None
    min_rooms: Optional[int] = None
    min_toilets: Optional[int] = None
    min_parking: Optional[int] = None
    required_facilities: Optional[str] = None
    required_surroundings: Optional[str] = None
    min_budget: Optional[int] = None
    max_budget: Optional[int] = None
    min_deposit: Optional[int] = None
    max_deposit: Optional[int] = None
    min_rent: Optional[int] = None
    max_rent: Optional[int] = None
    max_maintenance: Optional[int] = None
    max_premium: Optional[int] = None
    notes: Optional[str] = None
    tags: Optional[str] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PropertyRequestBase(BaseModel):
    """Base property request schema."""
    title: str
    description: Optional[str] = None
    region_preference: str
    radius_km: Optional[int] = None
    urgency_level: Optional[str] = None
    contact_name: str
    contact_phone: str
    due_date: Optional[date] = None
    preferences: Optional[RequestPreferenceBase] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PropertyRequestCreate(PropertyRequestBase):
    """Property request creation schema."""
    pass


class PropertyRequestUpdate(BaseModel):
    """Property request update schema."""
    title: Optional[str] = None
    description: Optional[str] = None
    region_preference: Optional[str] = None
    radius_km: Optional[int] = None
    urgency_level: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[date] = None
    preferences: Optional[RequestPreferenceBase] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PropertyRequest(PropertyRequestBase):
    """Property request schema."""
    id: int
    franchise_id: int
    status: str
    is_deleted: bool
    created_at: date

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PropertyResponse(BaseModel):
    """Property response schema."""
    data: Property
    detail: Optional[PropertyDetail] = None
    message: Optional[str] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PropertyListResponse(BaseModel):
    """Property list response schema."""
    data: List[Property]
    total: int
    message: Optional[str] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class Property(Base):
    """Property model."""
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=False, default="South Korea")
    property_type = Column(Enum(PropertyType), nullable=False)
    status = Column(Enum(PropertyStatus), default=PropertyStatus.AVAILABLE, nullable=False)
    price = Column(Float, nullable=True)
    size = Column(Float, nullable=True)  # Size in square meters
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    year_built = Column(Integer, nullable=True)
    is_featured = Column(Boolean, default=False, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="properties")
    images = relationship("PropertyImage", back_populates="property", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="property", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="property", cascade="all, delete-orphan")
    contracts = relationship("Contract", back_populates="property", cascade="all, delete-orphan")


class PropertyImage(Base):
    """Property image model."""
    
    url = Column(String(255), nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)
    caption = Column(String(255), nullable=True)
    
    # Foreign keys
    property_id = Column(Integer, ForeignKey("property.id"), nullable=False)
    
    # Relationships
    property = relationship("Property", back_populates="images")


class Favorite(Base):
    """User's favorite property model."""
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("property.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="favorites")
    property = relationship("Property", back_populates="favorites")
