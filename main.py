from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.api.v1 import auth, otp
from fastapi.middleware.cors import CORSMiddleware

# DB yaratish
Base.metadata.create_all(bind=engine)

app = FastAPI(title="IshonchMulk")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routerlar
app.include_router(auth.router)
app.include_router(otp.router)
