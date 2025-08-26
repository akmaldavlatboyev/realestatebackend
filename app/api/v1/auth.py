from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.auth import RegisterRequest, LoginRequest, UserResponse

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """JWT token yaratish"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register", response_model=UserResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == request.phone).first()
    if not user or not user.is_verified:
        raise HTTPException(status_code=400, detail="Telefon raqam tasdiqlanmagan")

    if request.password != request.confirm_password:
        raise HTTPException(status_code=400, detail="Parollar mos emas")

    hashed_password = pwd_context.hash(request.password)

    user.first_name = request.first_name
    user.last_name = request.last_name
    user.password = hashed_password
    user.role = UserRole.xaridor

    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.phone == request.phone).first()

    
    if not user:
        raise HTTPException(status_code=401, detail="Telefon raqam ro‘yxatdan o‘tmagan")

    
    if not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=401, detail="Parol noto‘g‘ri")

    if not user.is_verified:
        raise HTTPException(status_code=401, detail="Telefon raqamingiz tasdiqlanmagan")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_me(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token yaroqsiz")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token yaroqsiz")

    user = db.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    return user
