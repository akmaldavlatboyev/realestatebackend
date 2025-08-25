import enum
from sqlalchemy import Column, Integer, String, Enum, Boolean, Float
from app.db.base import Base

class UserRole(str, enum.Enum):
    xaridor = "xaridor"
    sotuvchi = "sotuvchi"
    makler = "makler"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    password = Column(String, nullable=True)  # hashed password
    role = Column(Enum(UserRole), nullable=False, default=UserRole.xaridor)
    is_verified = Column(Boolean, default=False)  # telefon tasdiqlanganmi
    sms_sent_today = Column(Integer, default=0)  # bugungi yuborilgan SMSlar
    sms_balance = Column(Float, default=1.0)    # foydalanuvchi balans
