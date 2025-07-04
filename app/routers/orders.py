from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.db import SessionLocal
from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderReceipt
from app.dependencies import get_current_user

router = APIRouter(prefix="/purchase", tags=["orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/{product_id}",
    response_model=OrderReceipt,
    summary="Purchase Product",
    description="Create an order for a single product and return the receipt information. Requires Authorization header."
)
def purchase_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    order = Order(
        user_id=current_user.id,
        product_id=product.id,
        purchase_time=datetime.utcnow()
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    return OrderReceipt(
        order_id=order.id,
        product_id=product.id,
        purchase_time=order.purchase_time
    )