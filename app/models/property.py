from enum import Enum
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum as SQLAlchemyEnum, Date
from sqlalchemy.orm import relationship
from config.database import Base

class PropertyStatus(str, Enum):
    """Property status enum."""
    AVAILABLE = "available"
    PENDING = "pending"
    SOLD = "sold"

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