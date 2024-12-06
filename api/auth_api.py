from flask import Blueprint, request, jsonify
from models.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, app
from datetime import datetime, timedelta
from controllers.email_controller import send_email
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity
)


import random
import os

auth_api_blueprint = Blueprint('auth_api', __name__, url_prefix='/api/auth')

# Konfigurasi JWT di app utama (app.py)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Gantilah dengan key yang lebih aman

# Login API
@auth_api_blueprint.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email dan password tidak boleh kosong.'}), 400

    user = User.query.filter_by(email=email).first()

    if user:
        if user.role != 'public':
            return jsonify({'message': 'Hanya akun dengan role public yang dapat login.'}), 403

        if not user.is_verified:
            return jsonify({'message': 'Akun Anda belum diverifikasi. Silakan verifikasi email Anda.'}), 400

        if check_password_hash(user.password_hash, password):
            # Buat token akses dan refresh
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            return jsonify({
                'message': 'Login berhasil!',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': user.id,
                    'nama_user': user.nama_user,
                    'email': user.email,
                    'role': user.role,
                }
            }), 200
        else:
            return jsonify({'message': 'Password salah!'}), 400
    else:
        return jsonify({'message': 'Email tidak terdaftar.'}), 400


# Register API
@auth_api_blueprint.route('/register', methods=['POST'])
def api_register():
    try:
        data = request.get_json()

        nama_user = data.get('nama_user')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if len(password) < 8:
            return jsonify({'message': 'Password harus memiliki minimal 8 karakter!'}), 400

        if '@' not in email or '.' not in email.split('@')[-1]:
            return jsonify({'message': 'Format email tidak valid!'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'Email sudah terdaftar!'}), 400
        elif password != confirm_password:
            return jsonify({'message': 'Password tidak cocok!'}), 400
        else:
            otp = random.randint(100000, 999999)
            otp_expiry = datetime.now() + timedelta(seconds=90)

            # Set role ke 'public' secara default
            new_user = User(
                nama_user=nama_user,
                email=email,
                role='public',
                password_hash=generate_password_hash(password),
                is_verified=False,
                otp=otp,
                otp_expiry=otp_expiry
            )

            db.session.add(new_user)
            db.session.commit()

            subject = "Verifikasi Akun Anda"
            body = f"<p>Kode OTP Anda: <b>{otp}</b>. Berlaku selama 1 menit 30 detik.</p>"
            send_email(subject, body, email)

            return jsonify({'message': 'OTP telah dikirim ke email Anda.'}), 200
    except Exception as e:
        # Tangani error dan log error untuk debugging
        app.logger.error(f"Error during registration: {e}")
        return jsonify({'message': 'Terjadi kesalahan di server.'}), 500



# Endpoint untuk mendapatkan token baru menggunakan refresh token
@auth_api_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': new_access_token}), 200


# Endpoint contoh yang dilindungi JWT
@auth_api_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)

    if not user:
        return jsonify({'message': 'Pengguna tidak ditemukan!'}), 404

    return jsonify({
        'message': f'Hello, {user.nama_user}!',
        'user': {
            'id': user.id,
            'email': user.email,
            'role': user.role
        }
    }), 200
