from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from config.database import get_db
from app.service.property_service import PropertyService
from app.schemas.property import (
    PropertyCreate,
    PropertyResponse,
    PropertyListResponse,
    PropertyDetailResponse
)
# from app.core.auth import get_current_user
from app.schemas.user import User

router = APIRouter(
    prefix="/properties",
    tags=["properties"]
)

@router.post("", response_model=PropertyResponse)
async def create_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new property listing."""
    property = await PropertyService.create_property(db, property_data, current_user.id)
    return PropertyResponse(
        data=property,
        message="Property created successfully"
    )

@router.get("", response_model=PropertyListResponse)
async def get_properties(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    agent_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get list of properties."""
    properties, total = await PropertyService.get_properties(db, skip, limit, agent_id)
    return PropertyListResponse(
        data=properties,
        total=total,
        message="Properties retrieved successfully"
    )

@router.get("/{property_id}", response_model=PropertyDetailResponse)
async def get_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific property by ID."""
    property = await PropertyService.get_property(db, property_id)
    return PropertyDetailResponse(
        data=property,
        message="Property retrieved successfully"
    ) 