import random
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
def generate_otp():
    return str(random.randint(100000, 999999))

def send_telegram_otp(otp):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": f"🔐 Your OTP is: {otp}"
    }
    requests.post(url, data=payload)
