from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.user import User
from app.models.order import Order
from app.schemas.user import UserRead
from app.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "/profile",
    summary="Get User Profile and Transaction Count",
    description="Return the current user's info and their transaction count (orders), using the token for authentication. Returns: { 'user': UserRead, 'transaction_count': int }"
)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    count = db.query(Order).filter(Order.user_id == current_user.id).count()
    return {
        "user": UserRead.from_orm(current_user),
        "transaction_count": count
    } 