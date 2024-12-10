from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, current_app
)
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db , app
from datetime import datetime, timedelta
from controllers.email_controller import send_email
import random
from flask import make_response  , url_for


auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password')
        remember = request.form.get('remember')  

        # Validasi input
        if not email or not password:
            flash('Email dan password tidak boleh kosong.', 'danger')
            return redirect(url_for('auth.login'))

        # Ambil user berdasarkan email
        user = User.query.filter_by(email=email).first()

        if user:
            # Cek apakah role user adalah 'public'
            if user.role == 'public':
                flash('Anda harus login melalui aplikasi mobile.', 'warning')
                return redirect(url_for('auth.login'))  # Tetap di halaman login

            # Cek apakah akun sudah diverifikasi
            if not user.is_verified:
                session['email_to_verify'] = email
                flash('Akun Anda belum diverifikasi. Silakan verifikasi email Anda.', 'warning')
                return redirect(url_for('auth.verify_email'))

            # Validasi password
            if check_password_hash(user.password_hash, password):
                # Buat URL untuk avatar
                avatar_url = (
                    url_for('static', filename=f'uploads/avatars/{user.avatar}', _external=True)
                    if user.avatar else
                    url_for('static', filename='uploads/avatars/default-avatar.png', _external=True)
                )

                # Simpan data session user
                session['user'] = {
                    'id': user.id,
                    'nama_user': user.nama_user,
                    'email': user.email,
                    'role': user.role,
                    'avatar': avatar_url,  # Tambahkan URL avatar ke session
                }

                # Jika "Ingat Saya" tidak dicentang, jadikan session sementara
                if not remember:
                    session.permanent = False  # Session akan berakhir saat browser ditutup
                else:
                    session.permanent = True  # Session akan bertahan
                    current_app.permanent_session_lifetime = timedelta(days=30)  # Misal, 30 hari

                # Redirect berdasarkan role
                return redirect(url_for('admin.dashboard' if user.role in ['admin', 'superadmin'] else 'auth.login'))
            else:
                flash('Password salah!', 'danger')
        else:
            flash('Email tidak terdaftar.', 'danger')

    return render_template('page/login-page.html')

@auth_blueprint.before_app_request
def check_remember_me():
    """Middleware untuk mengecek cookie 'remember_token' jika user belum login."""
    if 'user' not in session:
        remember_token = request.cookies.get('remember_token')
        if remember_token:
            user = User.query.filter_by(email=remember_token).first()
            if user:
                session['user'] = {
                    'id': user.id,
                    'nama_user': user.nama_user,
                    'email': user.email,
                    'role': user.role,
                }
            else:
                # Jika token tidak valid, hapus cookie
                response = make_response(redirect(url_for('auth.login')))
                response.set_cookie('remember_token', '', expires=0)
                return response

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nama_user = request.form['nama_user']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validasi panjang password
        if len(password) < 8:
            flash('Password harus memiliki minimal 8 karakter!', 'danger')
            return redirect(url_for('auth.register'))

        # Validasi email format
        if '@' not in email or '.' not in email.split('@')[-1]:
            flash('Format email tidak valid!', 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash('Email sudah terdaftar!', 'danger')
        elif password != confirm_password:
            flash('Password tidak cocok!', 'danger')
        else:
            otp = random.randint(100000, 999999)
            otp_expiry = datetime.now() + timedelta(seconds=90)
            new_user = User(
                nama_user=nama_user,
                email=email,
                role='admin',
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

            session['email_to_verify'] = email
            flash('OTP telah dikirim ke email Anda.', 'info')
            return redirect(url_for('auth.verify_email'))

    return render_template('page/register-page.html')


@auth_blueprint.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    email_to_verify = session.get('email_to_verify')
    if not email_to_verify:
        flash('Tidak ada email yang diverifikasi.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email_to_verify).first()
    if not user:
        flash('Pengguna tidak ditemukan.', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        otp_input = request.form['otp']
        if not otp_input.isdigit():
            flash('Kode OTP hanya boleh berisi angka.', 'danger')
            return redirect(url_for('auth.verify_email'))

        if user.otp != int(otp_input) or user.otp_expiry < datetime.now():
            flash('Kode OTP tidak valid atau telah kedaluwarsa.', 'danger')
            return redirect(url_for('auth.verify_email'))

        user.is_verified = True
        user.otp = None
        user.otp_expiry = None
        db.session.commit()
        session.pop('flash_verify_email', None)
        flash('Akun Anda berhasil diverifikasi!', 'success')
        return redirect(url_for('auth.login'))

    remaining_time = (
        max(0, int((user.otp_expiry - datetime.now()).total_seconds()))
        if user and user.otp_expiry else 0
    )
    return render_template('page/verify-email-page.html', remaining_time=remaining_time)

@auth_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()  # Hapus semua data session
    response = make_response(redirect(url_for('public.home')))
    response.set_cookie('remember_token', '', expires=0)  # Hapus cookie
    return response




