from pydantic import BaseModel, Field
from typing import Literal, Optional

class CountryRead(BaseModel):
    id: int
    name: str
    iso: str
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    title: str = Field(..., description="The name of the product")
    description: str = Field(..., description="Detailed description of the product")
    price: float = Field(..., description="Price of the product in USD")
    location: str = Field(..., description="Geographical availability (ISO code, e.g., JO for Jordan, SA for Saudi Arabia)")

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int
    country: Optional[CountryRead]
    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "title": "FIFA 23 Ultimate Edition",
                    "description": "Digital game code for PlayStation 5.",
                    "price": 59.99,
                    "location": "JO",
                    "country": {
                        "id": 1,
                        "name": "Jordan",
                        "iso": "JO"
                    }
                }
            ]
        } 