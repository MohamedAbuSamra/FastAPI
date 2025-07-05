from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserRead
from app.schemas.product import ProductRead

class OrderBase(BaseModel):
    user_id: int
    product_id: int

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int
    purchase_time: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "examples": [
                {
                    "id": 1,
                    "user_id": 2,
                    "product_id": 3,
                    "purchase_time": "2024-07-05T12:34:56"
                }
            ]
        }

class OrderReceipt(BaseModel):
    order_id: int
    product_id: int
    purchase_time: datetime

class OrderFullReceipt(BaseModel):
    order_id: int
    user: UserRead
    product: ProductRead
    price: float
    purchase_time: datetime 