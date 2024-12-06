from flask import Blueprint, request, jsonify
from models.models import User
from app import db
from datetime import datetime, timedelta
import random
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Konfigurasi Email
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Blueprint untuk API Resend Email
resend_email_blueprint = Blueprint('resend_email', __name__, url_prefix='/api/resend')

# Fungsi Kirim Email
def send_email(subject, body, recipient_email):
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
        print(f"Error sending email: {e}")
        raise

# Endpoint Resend OTP
@resend_email_blueprint.route('/resend-otp', methods=['POST'])
def resend_otp():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'success': False, 'message': 'Email tidak boleh kosong.'}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'success': False, 'message': 'Pengguna tidak ditemukan.'}), 404

    if user.is_verified:
        return jsonify({'success': False, 'message': 'Akun Anda sudah terverifikasi.'}), 400

    # Cek apakah OTP masih aktif
    if user.otp_expiry and user.otp_expiry > datetime.now():
        remaining_time = int((user.otp_expiry - datetime.now()).total_seconds())
        return jsonify({
            'success': False,
            'message': 'Kode OTP masih aktif. Tunggu hingga kedaluwarsa.',
            'remaining_time': remaining_time
        }), 400

    # Generate OTP baru
    otp = random.randint(100000, 999999)
    user.otp = otp
    user.otp_expiry = datetime.now() + timedelta(seconds=90)  # 1 menit 30 detik
    db.session.commit()

    try:
        subject = "Kode OTP Baru Anda"
        body = f"<p>Kode OTP baru Anda adalah <b>{otp}</b>. Berlaku selama 1 menit 30 detik.</p>"
        send_email(subject, body, user.email)
        return jsonify({'success': True, 'remaining_time': 90}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'Gagal mengirim ulang OTP.'}), 500
