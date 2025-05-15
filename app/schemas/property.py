from typing import Optional
from datetime import date
from pydantic import BaseModel, confloat, conint
from models.property import PropertyStatus

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

class Property(PropertyBase):
    """Property schema (response)."""
    id: int
    status: PropertyStatus
    is_deleted: bool
    agent_id: int
    created_at: date

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class PropertyDetail(Property):
    """Property detail schema with agent information."""
    agent_name: Optional[str] = None
    agent_phone: Optional[str] = None
    agent_email: Optional[str] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class PropertyResponse(BaseModel):
    """API response schema for property operations."""
    data: Property
    message: Optional[str] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class PropertyDetailResponse(BaseModel):
    """API response schema for property detail operations."""
    data: PropertyDetail
    message: Optional[str] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class PropertyListResponse(BaseModel):
    """API response schema for multiple properties."""
    data: list[Property]
    total: int
    message: Optional[str] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True 