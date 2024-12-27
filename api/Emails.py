from flask import Blueprint, request, jsonify, session
from models.user import User
from app import db
from datetime import datetime, timedelta
import random
from utils.EmailUtils import send_email

# Blueprint untuk Email
email_blueprint = Blueprint('email', __name__, url_prefix='/email')

# Resend OTP
@email_blueprint.route('/resend-otp', methods=['POST'])
def resend_otp():
    """API untuk mengirim ulang kode OTP."""
    email_to_verify = session.get('email_to_verify')
    user = User.query.filter_by(email=email_to_verify).first()

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
        return jsonify({'success': False, 'message': 'Gagal mengirim ulang OTP.', 'error': str(e)}), 500
