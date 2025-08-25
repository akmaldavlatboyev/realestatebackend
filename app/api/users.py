# app/api/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead
from app.crud.user import create_user, get_user_by_phone

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_phone(db, user.phone):
        raise HTTPException(status_code=400, detail="Phone already registered")
    return create_user(db, user)
