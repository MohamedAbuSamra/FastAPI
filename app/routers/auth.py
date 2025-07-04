from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db import SessionLocal
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.schemas.user import UserLogin, UserRead
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.core.config import settings

router = APIRouter(prefix="", tags=["auth"])

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserRead

class LoginRequest(BaseModel):
    username: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/login",
    response_model=Token,
    summary="Login",
    description="""
Authenticate a user and return a JWT access token.\n\n**You can use either of the following:**\n\n**1. JSON body:**\n```json\n{\n  \"username\": \"your_username\",\n  \"password\": \"your_password\"\n}\n```\n\n**2. Form data (application/x-www-form-urlencoded):**\n- username: your_username\n- password: your_password\n"""
)
async def login(request: Request, db: Session = Depends(get_db)):
    if request.headers.get("content-type", "").startswith("application/json"):
        body = await request.json()
        username = body.get("username")
        password = body.get("password")
    else:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Missing username or password")

    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    access_token = create_access_token({"sub": str(user.id)})
    user_info = UserRead.from_orm(user)
    print(f"[LOGIN] Token for user '{username}' will expire at: {expire.isoformat()} UTC (in {expire_minutes} minute(s))")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_info,
        "message": f"This token will be invalid in {expire_minutes} minute(s) based on the environment setting."
    }