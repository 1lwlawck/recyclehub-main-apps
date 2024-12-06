from flask import Blueprint, request, jsonify, url_for
from models.models import User
from app import db
from datetime import datetime, timedelta
import random
from controllers.email_controller import send_email

password_api_blueprint = Blueprint('password_api', __name__, url_prefix='/api/password')

@password_api_blueprint.route('/forgot', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'success': False, 'message': 'Email tidak boleh kosong.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'success': False, 'message': 'Email tidak terdaftar.'}), 404

    # Generate reset token
    reset_token = random.randint(100000, 999999)
    reset_token_expiry = datetime.now() + timedelta(minutes=30)
    user.reset_token = str(reset_token)
    user.reset_token_expiry = reset_token_expiry
    db.session.commit()

    # Kirim email
    reset_link = url_for('password_api.reset_password', token=reset_token, _external=True)
    subject = "Permintaan Reset Password"
    body = f"<p>Klik link berikut untuk reset password Anda: <a href='{reset_link}'>Reset Password</a></p>"
    send_email(subject, body, email)

    return jsonify({'success': True, 'message': 'Email reset password telah dikirim.'}), 200


@password_api_blueprint.route('/reset/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json()
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    if not new_password or not confirm_password:
        return jsonify({'success': False, 'message': 'Password tidak boleh kosong.'}), 400

    if new_password != confirm_password:
        return jsonify({'success': False, 'message': 'Password baru dan konfirmasi tidak cocok.'}), 400

    # Cari user berdasarkan token
    user = User.query.filter_by(reset_token=token).first()
    if not user or user.reset_token_expiry < datetime.now():
        return jsonify({'success': False, 'message': 'Token tidak valid atau telah kedaluwarsa.'}), 400

    # Update password
    user.password_hash = generate_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    db.session.commit()

    return jsonify({'success': True, 'message': 'Password berhasil direset.'}), 200
