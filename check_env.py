from dotenv import load_dotenv
import os

# .env faylni yuklash
load_dotenv()

# O'qilgan qiymatni ko‘rish
print("DATABASE_URL from .env:", os.getenv("DATABASE_URL"))
