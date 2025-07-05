from sqlalchemy import Column, Integer, String
from app.db import Base

class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    iso = Column(String(2), unique=True, nullable=False, index=True) 