from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import User
from app import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from controllers.email_controller import send_email
import random

password_blueprint = Blueprint('password', __name__, url_prefix='/password')

@password_blueprint.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email').strip()
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

    return render_template('page/input-email-page.html')

@password_blueprint.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()

    if not user or user.reset_token_expiry < datetime.now():
        flash('Token tidak valid atau telah kedaluwarsa.', 'danger')
        return redirect(url_for('password.forgot_password'))

    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if not new_password or new_password != confirm_password:
            flash('Password tidak cocok atau kosong.', 'danger')
            return redirect(url_for('password.reset_password', token=token))

        user.password_hash = generate_password_hash(new_password)
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()

        flash('Password berhasil direset.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('page/reset-password-page.html', token=token)
