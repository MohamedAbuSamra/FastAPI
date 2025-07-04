from pydantic import BaseModel, Field
from typing import Literal

class ProductBase(BaseModel):
    title: str = Field(..., description="The name of the product", example="FIFA 23 Ultimate Edition")
    description: str = Field(..., description="Detailed description of the product", example="Digital game code for PlayStation 5.")
    price: float = Field(..., description="Price of the product in USD", example=59.99)
    location: Literal["JO", "SA"] = Field(..., description="Geographical availability (JO for Jordan, SA for Saudi Arabia)", example="JO")

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int

    class Config:
        orm_mode = True 