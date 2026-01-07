import random
import smtplib
import os
import requests
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
def generate_otp():
    return str(random.randint(100000, 999999))

def send_email_otp(receiver_email, otp):
    msg = MIMEText(f"Your OTP for Emotion Classifier Login is: {otp}")
    msg["Subject"] = "OTP Verification"
    msg["From"] = EMAIL_USER
    msg["To"] = receiver_email
    print("EMAIL:", EMAIL_USER)
    print("PASS:", "LOADED" if EMAIL_PASS else "NOT LOADED")


    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

def send_telegram_otp(otp):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": f"🔐 Your OTP is: {otp}"
    }
    requests.post(url, data=payload)
