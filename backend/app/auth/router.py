from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest, TokenResponse, SignupRequest, SignupResponse
from app.db.crud.user import get_user_by_username
from app.auth.utils import verify_password
from app.auth.security import create_access_token
from app.dependencies.database import get_db
from app.schemas.auth import SignupRequest, TokenResponse
from app.auth.utils import hash_password
from app.db.crud.user import create_new_user

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = await get_user_by_username(db, payload.username)

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=token)  # 🧠 Use response model



@router.post("/signup", response_model=SignupResponse)
async def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing_user = await get_user_by_username(db, payload.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = hash_password(payload.password)
    user = await create_new_user(db, payload.username, payload.email, hashed)
    return SignupResponse(message="Thank you for signing up! Go ahead and login!")

