from sqlalchemy import Column, Integer, String, Float, Enum
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