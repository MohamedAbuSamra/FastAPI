from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from typing import List

from app.db import SessionLocal
from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderFullReceipt
from app.schemas.user import UserRead
from app.schemas.product import ProductRead
from app.dependencies import get_current_user

router = APIRouter(prefix="/purchase", tags=["orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PurchaseRequest(BaseModel):
    productId: int

@router.post(
    "/",
    response_model=OrderFullReceipt,
    summary="Purchase Product",
    description="Create an order for a single product and return the full receipt information. Requires Authorization header. Expects JSON body: { 'productId': int }"
)
def purchase_product(
    req: PurchaseRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product_id = req.productId
    print(f"[LOG] Received purchase request: product_id={product_id}, user_id={current_user.id}, username={current_user.username}")
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    order = Order(
        user_id=current_user.id,
        product_id=product.id,
        created_at=datetime.utcnow(),
        price=product.price,
        updated_at=datetime.utcnow(),
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return OrderFullReceipt(
        order_id=order.id,
        user=UserRead.from_orm(current_user),
        product=ProductRead.from_orm(product),
        price=order.price,
        purchase_time=order.created_at
    )

@router.get(
    "/transaction",
    response_model=OrderFullReceipt,
    summary="Get Order Transaction",
    description="Retrieve a transaction (order) by its ID. Returns the full receipt information."
)
def get_transaction(
    id: int = Query(..., description="Order ID"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found for this order")
    return OrderFullReceipt(
        order_id=order.id,
        user=UserRead.from_orm(current_user),
        product=ProductRead.from_orm(product),
        price=order.price,
        purchase_time=order.created_at
    )

@router.get(
    "/transactions/{id}",
    response_model=OrderFullReceipt,
    summary="Get Order Transaction (by path)",
    description="Retrieve a transaction (order) by its ID using a path parameter. Returns the full receipt information."
)
def get_transaction_by_path(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found for this order")
    return OrderFullReceipt(
        order_id=order.id,
        user=UserRead.from_orm(current_user),
        product=ProductRead.from_orm(product),
        price=order.price,
        purchase_time=order.created_at
    )

@router.get(
    "/transactions",
    response_model=List[OrderFullReceipt],
    summary="List All Transactions for Current User",
    description="Retrieve all transactions (orders) for the current user. Returns a list of full receipt objects."
)
def list_transactions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    results = []
    for order in orders:
        product = db.query(Product).filter(Product.id == order.product_id).first()
        if not product:
            continue  # skip if product not found
        results.append(OrderFullReceipt(
            order_id=order.id,
            user=UserRead.from_orm(current_user),
            product=ProductRead.from_orm(product),
            price=order.price,
            purchase_time=order.created_at
        ))
    return results