from enum import Enum
from typing import List, Optional
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum as SQLAlchemyEnum, Date
from sqlalchemy.orm import relationship
from config.database import Base


class PropertyType(str, Enum):
    """Property type enum."""
    
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    LAND = "land"
    OFFICE = "office"
    RETAIL = "retail"
    RESTAURANT = "restaurant"
    WAREHOUSE = "warehouse"
    OTHER = "other"
    APARTMENT = "apartment"
    HOUSE = "house"


class PropertyStatus(str, Enum):
    """Property status enum."""
    
    AVAILABLE = "available"
    SOLD = "sold"
    RENTED = "rented"
    PENDING = "pending"
    OFF_MARKET = "offMarket"


class PropertyImageBase(BaseModel):
    """Base property image schema."""
    
    url: str
    is_primary: bool = False
    caption: Optional[str] = None


class PropertyImageCreate(PropertyImageBase):
    """Property image creation schema."""
    
    pass


class PropertyImageUpdate(PropertyImageBase):
    """Property image update schema."""
    
    url: Optional[str] = None
    is_primary: Optional[bool] = None


class PropertyBase(BaseModel):
    """Base property schema."""
    
    title: str
    description: Optional[str] = None
    address: str
    city: str
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: str = "South Korea"
    property_type: PropertyType
    status: PropertyStatus = PropertyStatus.AVAILABLE
    price: Optional[float] = None
    size: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    year_built: Optional[int] = None
    is_featured: bool = False
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class PropertyCreate(PropertyBase):
    """Property creation schema."""
    
    images: Optional[List[PropertyImageCreate]] = None


class PropertyUpdate(BaseModel):
    """Property update schema."""
    
    title: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    property_type: Optional[PropertyType] = None
    status: Optional[PropertyStatus] = None
    price: Optional[float] = None
    size: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    year_built: Optional[int] = None
    is_featured: Optional[bool] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class PropertyImage(PropertyImageBase):
    """Property image schema."""
    
    id: int
    property_id: int
    
    class Config:
        orm_mode = True


class Property(Base):
    """Property database model."""
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    address = Column(String(500))
    region_code = Column(String(10))
    area_m2 = Column(Float)
    area_pyeong = Column(Float)
    deposit = Column(Integer)
    monthly_rent = Column(Integer)
    sale_price = Column(Integer)
    management_fee = Column(Integer)
    floor = Column(Integer)
    building_type = Column(String(100))
    year_built = Column(Integer)
    renovated = Column(Boolean)
    available_from = Column(Date)
    status = Column(SQLAlchemyEnum(PropertyStatus), default=PropertyStatus.AVAILABLE)
    is_deleted = Column(Boolean, default=False)
    agent_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    agent = relationship("User", back_populates="properties")

    def __repr__(self):
        return f"<Property {self.title}>"


class PropertyRequest(Base):
    """Property request database model."""
    __tablename__ = "property_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    franchise_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255))
    description = Column(Text)
    region_preference = Column(String(255))
    radius_km = Column(Integer)
    urgency_level = Column(String(50))
    contact_name = Column(String(100))
    contact_phone = Column(String(50))
    status = Column(String(50))  # pending, in_progress, completed, cancelled
    is_deleted = Column(Boolean, default=False)
    due_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    franchise = relationship("User", back_populates="property_requests")
    preferences = relationship("RequestPreference", back_populates="request", cascade="all, delete-orphan")


class RequestPreference(Base):
    """Request preference database model."""
    __tablename__ = "request_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(Integer, ForeignKey("property_requests.id"))
    property_type = Column(String(100))
    transaction_type = Column(String(50))
    category = Column(String(100))
    min_area = Column(Float)
    max_area = Column(Float)
    min_floor = Column(Integer)
    min_rooms = Column(Integer)
    min_toilets = Column(Integer)
    min_parking = Column(Integer)
    required_facilities = Column(Text)
    required_surroundings = Column(Text)
    min_budget = Column(Integer)
    max_budget = Column(Integer)
    min_deposit = Column(Integer)
    max_deposit = Column(Integer)
    min_rent = Column(Integer)
    max_rent = Column(Integer)
    max_maintenance = Column(Integer)
    max_premium = Column(Integer)
    notes = Column(Text)
    tags = Column(Text)

    # Relationships
    request = relationship("PropertyRequest", back_populates="preferences")


class PropertyResponse(BaseModel):
    property: Property
    message: Optional[str] = None

    class Config:
        orm_mode = True


class PropertyListResponse(BaseModel):
    properties: List[Property]
    total: int
    message: Optional[str] = None

    class Config:
        orm_mode = True
