from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, func
from app.db import Base
import enum

class LocationEnum(str, enum.Enum):
    JO = "JO"
    SA = "SA"

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    location = Column(Enum(LocationEnum), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True) 