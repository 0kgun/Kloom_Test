from typing import Optional
from sqlalchemy.orm import Session
from app.models.property import Property
from app.schemas.property import PropertyCreate
from app.core.exceptions import NotFoundException, UnauthorizedException

class PropertyService:
    @staticmethod
    async def create_property(db: Session, property_data: PropertyCreate, agent_id: int) -> Property:
        """Create a new property listing."""
        db_property = Property(
            **property_data.dict(),
            agent_id=agent_id
        )
        db.add(db_property)
        db.commit()
        db.refresh(db_property)
        return db_property

    @staticmethod
    async def get_property(db: Session, property_id: int) -> Optional[Property]:
        """Get a property by ID."""
        property = db.query(Property).filter(
            Property.id == property_id,
            Property.is_deleted == False
        ).first()
        if not property:
            raise NotFoundException(detail="Property not found")
        return property

    @staticmethod
    async def get_properties(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        agent_id: Optional[int] = None
    ) -> tuple[list[Property], int]:
        """Get list of properties with optional filtering."""
        query = db.query(Property).filter(Property.is_deleted == False)
        
        if agent_id:
            query = query.filter(Property.agent_id == agent_id)
        
        total = query.count()
        properties = query.offset(skip).limit(limit).all()
        
        return properties, total

    # @staticmethod
    # async def check_property_owner(db: Session, property_id: int, agent_id: int) -> bool:
    #     """Check if the agent is the owner of the property."""
    #     property = await PropertyService.get_property(db, property_id)
    #     if property.agent_id != agent_id:
    #         raise UnauthorizedException(detail="Not authorized to modify this property")
    #     return True 