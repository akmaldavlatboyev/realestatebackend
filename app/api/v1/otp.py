from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from random import randint
from datetime import datetime, timedelta
from app.db.session import get_db
from app.models.user import User
from app.models.otp import OTPCode

router = APIRouter(prefix="/api/v1/otp", tags=["OTP"])

SMS_LIMIT_PER_DAY = 3
SMS_COST = 0.1

def send_sms_api(phone: str, code: str):
    # Bu yerga haqiqiy SMS API qo‘shiladi
    print(f"Sending SMS to {phone}: {code}")
    return True

@router.post("/send")
def send_otp(phone: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == phone).first()
    if not user:
        user = User(phone=phone, first_name="Temp", last_name="Temp", password="Temp")
        db.add(user)
        db.commit()
        db.refresh(user)

    today = datetime.utcnow().date()
    if user.sms_sent_today >= SMS_LIMIT_PER_DAY:
        raise HTTPException(status_code=400, detail="Bugungi SMS limiti tugadi")

    if user.sms_balance < SMS_COST:
        raise HTTPException(status_code=400, detail="SMS balans yetarli emas")

    code = f"{randint(100000,999999)}"
    otp = OTPCode(phone=phone, code=code, expires_at=datetime.utcnow() + timedelta(minutes=5))
    db.add(otp)

    user.sms_balance -= SMS_COST
    user.sms_sent_today += 1

    db.commit()
    db.refresh(user)

    send_sms_api(phone, code)
    return {"detail": "SMS yuborildi"}


@router.post("/verify")
def verify_otp(phone: str, code: str, db: Session = Depends(get_db)):
    otp = db.query(OTPCode).filter(OTPCode.phone == phone, OTPCode.code == code).first()
    if not otp or otp.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP noto‘g‘ri yoki muddati tugagan")

    user = db.query(User).filter(User.phone == phone).first()
    if not user:
        raise HTTPException(status_code=400, detail="Foydalanuvchi topilmadi")

    user.is_verified = True
    db.commit()
    return {"detail": "Telefon raqam tasdiqlandi"}
