from pydantic import BaseModel, Field
from typing import Literal

class ProductBase(BaseModel):
    title: str = Field(..., description="The name of the product")
    description: str = Field(..., description="Detailed description of the product")
    price: float = Field(..., description="Price of the product in USD")
    location: Literal["JO", "SA"] = Field(..., description="Geographical availability (JO for Jordan, SA for Saudi Arabia)")

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "title": "FIFA 23 Ultimate Edition",
                    "description": "Digital game code for PlayStation 5.",
                    "price": 59.99,
                    "location": "JO"
                }
            ]
        } 