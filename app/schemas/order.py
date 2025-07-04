from pydantic import BaseModel
from datetime import datetime

class OrderBase(BaseModel):
    user_id: int
    product_id: int

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int
    purchase_time: datetime

    class Config:
        orm_mode = True

class OrderReceipt(BaseModel):
    order_id: int
    product_id: int
    purchase_time: datetime 