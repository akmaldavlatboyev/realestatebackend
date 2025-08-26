from fastapi import FastAPI
from app.db import base
from app.db.session import engine
from app.api.v1 import auth
from app.api.v1.auth import router as auth_router
from app.api.v1 import otp
from fastapi.middleware.cors import CORSMiddleware
# DB yaratish
base.Base.metadata.create_all(bind=engine)

app = FastAPI(title="IshonchMulk")


# CORS middleware
origins = [
    "*"  # front-end IP yoki barcha IPlarga ruxsat
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# routerlar
app.include_router(otp.router)
app.include_router(auth.router)

