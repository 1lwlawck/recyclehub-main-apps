import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Ambil variabel dari .env
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(subject, body, recipient_email):
    """Fungsi untuk mengirim email menggunakan SMTP."""
    try:
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = recipient_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        raise Exception(f"Error sending email: {e}")
