from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import User
from app import db

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            if user.role == 'public':
                flash('Login hanya tersedia di aplikasi mobile untuk pengguna umum.', 'warning')
                return redirect(url_for('auth.login'))

            session['user'] = {'email': user.email, 'role': user.role}
            flash('Login berhasil!', 'success')

            if user.role == 'superadmin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
        else:
            flash('Email atau password salah!', 'danger')

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
            new_user = User(
                nama_user=nama_user,
                email=email,
                password_hash=User.hash_password(password),
                role='admin' 
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registrasi berhasil! Silakan login.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('page/register-page.html')

@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Logout berhasil!', 'success')
    return redirect(url_for('auth.login'))
