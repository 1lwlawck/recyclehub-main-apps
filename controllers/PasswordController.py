from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from models.user import User
from app import db
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from api.Emails import send_email
import random
from utils import login_required , role_required
from modules.forms import ForgotPasswordForm , ResetPasswordForm  # Import form

password_blueprint = Blueprint('password', __name__, url_prefix='/password')

@password_blueprint.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data.strip()
        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Email tidak terdaftar.', 'danger')
        else:
            reset_token = random.randint(100000, 999999)
            reset_token_expiry = datetime.now() + timedelta(minutes=30)
            user.reset_token = str(reset_token)
            user.reset_token_expiry = reset_token_expiry
            db.session.commit()

            reset_link = url_for('password.reset_password', token=reset_token, _external=True)
            subject = "Permintaan Reset Password"
            body = f"<p>Klik link berikut untuk reset password Anda: <a href='{reset_link}'>Reset Password</a></p>"
            send_email(subject, body, email)

            flash('Email reset password telah dikirim.', 'info')
            return redirect(url_for('auth.login'))

    return render_template('page/input-email-page.html', form=form)


@password_blueprint.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()

    if not user or user.reset_token_expiry < datetime.now():
        flash('Token tidak valid atau telah kedaluwarsa.', 'danger')
        return redirect(url_for('password.forgot_password'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        new_password = form.new_password.data
        user.password_hash = generate_password_hash(new_password)
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()

        flash('Password berhasil direset.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('page/reset-password-page.html', form=form)


@password_blueprint.route('/change-password', methods=['POST'])
@login_required
def change_password():
    # Ambil data dari form
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    # Validasi input
    if not current_password or not new_password or not confirm_password:
        flash('Semua field wajib diisi.', 'change_password_error')
        return redirect(url_for('admin.settings'))

    # Ambil user dari session
    user = User.query.filter_by(email=session['user']['email']).first()
    if not user:
        flash('User tidak ditemukan.', 'change_password_error')
        return redirect(url_for('admin.settings'))

    # Validasi password lama
    if not check_password_hash(user.password_hash, current_password):
        flash('Password lama salah.', 'change_password_error')
        return redirect(url_for('admin.settings'))

    # Validasi password baru dan konfirmasi
    if new_password != confirm_password:
        flash('Password baru dan konfirmasi tidak cocok.', 'change_password_error')
        return redirect(url_for('admin.settings'))

    # Update password di database
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    flash('Password berhasil diubah.', 'change_password_success')
    return redirect(url_for('admin.settings'))