from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime, timedelta
from controllers.email_controller import send_email
import random

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password')

        if not email or not password:
            flash('Email dan password tidak boleh kosong.', 'danger')
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(email=email).first()

        if user:
            # Cek apakah akun sudah diverifikasi
            if not user.is_verified:
                session['email_to_verify'] = email
                flash('Akun Anda belum diverifikasi. Silakan verifikasi email Anda.', 'warning')
                return redirect(url_for('auth.verify_email'))

            # Validasi password
            if check_password_hash(user.password_hash, password):
                # Simpan data session user
                session['user'] = { 'id': user.id, 'nama_user': user.nama_user, 'email': user.email, 'role': user.role  }
                

                # Logika role-based redirect
                if user.role == 'superadmin':
                    return redirect(url_for('admin.dashboard'))
                elif user.role == 'admin':
                    return redirect(url_for('admin.dashboard'))
                else:
                    flash('Anda tidak memiliki izin untuk mengakses halaman ini.', 'danger')
                    return redirect(url_for('auth.login'))
            else:
                flash('Password salah!', 'danger')
        else:
            flash('Email tidak terdaftar.', 'danger')

    return render_template('page/login-page.html')


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nama_user = request.form['nama_user']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

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
    session.clear()
    return redirect(url_for('public.home'))


