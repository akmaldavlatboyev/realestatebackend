from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL .env faylda topilmadi")

# Render PostgreSQL uchun SSL kerak bo'lishi mumkin
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}  # Renderda SSL bilan ulanadi
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
