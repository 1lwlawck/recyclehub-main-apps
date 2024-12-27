from flask import Blueprint, request, jsonify , session , url_for
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, app
from datetime import datetime, timedelta
from api.Emails import send_email
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity
)

import random
import os
import logging

auth_api_blueprint = Blueprint('auth_api', __name__, url_prefix='/api/auth')

# Menambahkan logging untuk memeriksa apakah session dapat diakses
logging.basicConfig(level=logging.DEBUG)

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


@auth_api_blueprint.route('/register', methods=['POST'])
def api_register():
    data = request.get_json()

    # Validasi input
    if not data.get('nama_user') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Nama, email, dan password wajib diisi'}), 400

    nama_user = data['nama_user']
    email = data['email']
    password = data['password']
    confirm_password = data.get('confirm_password')

    # Validasi panjang password
    if len(password) < 8:
        return jsonify({'error': 'Password harus memiliki minimal 8 karakter'}), 400

    # Validasi email format
    if '@' not in email or '.' not in email.split('@')[-1]:
        return jsonify({'error': 'Format email tidak valid'}), 400

    # Cek apakah email sudah terdaftar
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email sudah terdaftar'}), 400

    # Cek password dan confirm password
    if password != confirm_password:
        return jsonify({'error': 'Password dan konfirmasi password tidak cocok'}), 400

    # Generate OTP
    otp = random.randint(100000, 999999)
    otp_expiry = datetime.now() + timedelta(seconds=90)  # 1 menit 30 detik

    # Simpan user dengan status belum diverifikasi
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

    # Kirim OTP ke email
    subject = "Verifikasi Akun Anda"
    body = f"<p>Kode OTP Anda: <b>{otp}</b>. Berlaku selama 1 menit 30 detik.</p>"
    send_email(subject, body, email)

    return jsonify({'message': 'OTP telah dikirim ke email Anda, silakan verifikasi'}), 200


# Endpoint untuk verifikasi OTP
@auth_api_blueprint.route('/verify-otp', methods=['POST'])
def api_verify_otp():
    data = request.get_json()

    # Validasi input
    if not data.get('email') or not data.get('otp'):
        return jsonify({'error': 'Email dan OTP wajib diisi'}), 400

    email = data['email']
    otp_input = data['otp']

    # Ambil user berdasarkan email
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Pengguna tidak ditemukan'}), 404

    # Cek apakah OTP valid dan belum kedaluwarsa
    if user.otp != int(otp_input) or user.otp_expiry < datetime.now():
        return jsonify({'error': 'OTP tidak valid atau telah kedaluwarsa'}), 400

    # Verifikasi akun pengguna
    user.is_verified = True
    user.otp = None
    user.otp_expiry = None
    db.session.commit()

    return jsonify({'message': 'Akun Anda berhasil diverifikasi'}), 200


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
