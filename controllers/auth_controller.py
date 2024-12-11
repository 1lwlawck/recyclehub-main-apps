from flask import (
    Blueprint, render_template, redirect, url_for, flash, session, current_app
)
from modules.forms import LoginForm , RegistrationForm , OTPForm # Import dari modules
from models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from app import db , app
from datetime import datetime , timedelta 
from flask import request , make_response 
from controllers.email_controller import send_email
import random


auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():  # Validasi form setelah submit
        email = form.email.data.strip()
        password = form.password.data
        remember = form.remember.data

        # Ambil user berdasarkan email
        user = User.query.filter_by(email=email).first()

        if user:
            # Cek apakah role user adalah 'public'
            if user.role == 'public':
                flash('Anda harus login melalui aplikasi mobile.', 'warning')
                return redirect(url_for('auth.login'))

            # Cek apakah akun sudah diverifikasi
            if not user.is_verified:
                session['email_to_verify'] = email
                flash('Akun Anda belum diverifikasi. Silakan verifikasi email Anda.', 'warning')
                return redirect(url_for('auth.verify_email'))

            # Validasi password
            if check_password_hash(user.password_hash, password):
                avatar_url = (
                    url_for('static', filename=f'uploads/avatars/{user.avatar}', _external=True)
                    if user.avatar else
                    url_for('static', filename='uploads/avatars/default-avatar.png', _external=True)
                )

                session['user'] = {
                    'id': user.id,
                    'nama_user': user.nama_user,
                    'email': user.email,
                    'role': user.role,
                    'avatar': avatar_url,
                }

                if not remember:
                    session.permanent = False
                else:
                    session.permanent = True
                    current_app.permanent_session_lifetime = timedelta(days=30)

                return redirect(url_for('admin.dashboard' if user.role in ['admin', 'superadmin'] else 'auth.login'))
            else:
                flash('Password salah!', 'danger')
        else:
            flash('Email tidak terdaftar.', 'danger')

    return render_template('page/login-page.html', form=form)


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
    form = RegistrationForm()

    if form.validate_on_submit():
        nama_user = form.nama_user.data
        email = form.email.data
        password = form.password.data

        # Cek apakah email sudah terdaftar
        if User.query.filter_by(email=email).first():
            flash('Email sudah terdaftar!', 'danger')
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

    return render_template('page/register-page.html', form=form)


@auth_blueprint.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    form = OTPForm()
    email_to_verify = session.get('email_to_verify')

    if not email_to_verify:
        flash('Tidak ada email yang diverifikasi.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email_to_verify).first()
    if not user:
        flash('Pengguna tidak ditemukan.', 'danger')
        return redirect(url_for('auth.login'))

    # Logika untuk tombol 'Kirim Ulang'
    if form.resend.data:
        if user.otp_expiry and user.otp_expiry > datetime.now():
            remaining_time = int((user.otp_expiry - datetime.now()).total_seconds())
            flash(f'Kode OTP masih aktif. Tunggu {remaining_time} detik.', 'warning')
        else:
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.otp_expiry = datetime.now() + timedelta(seconds=90)
            db.session.commit()

            subject = "Kode OTP Baru Anda"
            body = f"<p>Kode OTP baru Anda adalah <b>{otp}</b>. Berlaku selama 1 menit 30 detik.</p>"
            send_email(subject, body, user.email)
            flash('Kode OTP baru telah dikirim ke email Anda.', 'success')

        return redirect(url_for('auth.verify_email'))

    # Logika untuk validasi OTP
    if form.validate_on_submit() and form.submit.data:
        otp_input = form.otp.data
        if user.otp != int(otp_input) or user.otp_expiry < datetime.now():
            flash('Kode OTP tidak valid atau telah kedaluwarsa.', 'danger')
            return redirect(url_for('auth.verify_email'))

        user.is_verified = True
        user.otp = None
        user.otp_expiry = None
        db.session.commit()

        flash('Akun Anda berhasil diverifikasi!', 'success')
        return redirect(url_for('auth.login'))

    remaining_time = (
        max(0, int((user.otp_expiry - datetime.now()).total_seconds()))
        if user and user.otp_expiry else 0
    )

    return render_template('page/verify-email-page.html', form=form, remaining_time=remaining_time)


@auth_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()  # Hapus semua data session
    response = make_response(redirect(url_for('public.home')))
    response.set_cookie('remember_token', '', expires=0)  # Hapus cookie
    return response




