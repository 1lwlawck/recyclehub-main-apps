from flask import Blueprint, render_template, flash, abort, jsonify, session, redirect, url_for
from utils import login_required, role_required
from models.user import User, db 
from models.articles import Article
from datetime import datetime
from time import time
import os
from app import app

# Membuat Blueprint untuk Admin
admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

# Halaman Dashboard
@admin_blueprint.route('/dashboard')    
@login_required
@role_required(['admin', 'superadmin'])
def dashboard():
    try:
        jumlah_user = User.query.count()
        jumlah_admin = User.query.filter_by(role='admin').count()
        jumlah_superadmin = User.query.filter_by(role='superadmin').count()
        jumlah_user_public = User.query.filter_by(role='public').count()

        jumlah_artikel = Article.query.count()

        # Tambahkan logika jika diperlukan, misalnya statistik
        return render_template('admin/dashboard-admin.html' ,jumlah_user=jumlah_user, jumlah_admin=jumlah_admin, jumlah_superadmin=jumlah_superadmin, jumlah_user_public=jumlah_user_public, jumlah_artikel=jumlah_artikel, time=time)
        print("Session Avatar:", session['user']['avatar'])
    except Exception as e:
        flash('Terjadi kesalahan saat memuat halaman dashboard.', 'danger')
        return jsonify({'message': 'Error loading dashboard', 'error': str(e)}), 500

# Halaman Dropoff
@admin_blueprint.route('/dropoff')
@login_required
@role_required(['admin', 'superadmin'])
def dropoff():
    try:
        # Tambahkan logika jika diperlukan, misalnya data dropoff
        return render_template('admin/dropoff-admin.html' , time=time)
    except Exception as e:
        flash('Terjadi kesalahan saat memuat halaman dropoff.', 'danger' )
        return jsonify({'message': 'Error loading dropoff', 'error': str(e)}), 500

# Halaman Riwayat
@admin_blueprint.route('/riwayat')
@login_required
@role_required(['admin', 'superadmin'])
def riwayat():
    try:
        # Tambahkan logika jika diperlukan, misalnya data riwayat
        return render_template('admin/riwayat-admin.html' , time=time)
    except Exception as e:
        flash('Terjadi kesalahan saat memuat halaman riwayat.', 'danger' )
        return jsonify({'message': 'Error loading history', 'error': str(e)}), 500

# Halaman Pesan
@admin_blueprint.route('/message')
@login_required
@role_required(['admin', 'superadmin'])
def message():
    try:
        # Tambahkan logika jika diperlukan, misalnya data pesan
        return render_template('admin/message-admin.html' , time=time)
    except Exception as e:
        flash('Terjadi kesalahan saat memuat halaman pesan.', 'danger')
        return jsonify({'message': 'Error loading messages', 'error': str(e)}), 500

@admin_blueprint.route('/sentiment')
@login_required
@role_required(['superadmin'])
def sentiment_analysis():
    try:
        # Tambahkan logika jika diperlukan, misalnya data pesan
        return render_template('admin/sentiment-analysis.html' , time=time)
    except Exception as e:
        flash('Terjadi kesalahan saat memuat halaman sentiment.', 'danger')
        return jsonify({'message': 'Error loading sentiment', 'error': str(e)}), 500


# Halaman Manage User (Hanya untuk superadmin)
@admin_blueprint.route('/manage-user')
@login_required
@role_required(['superadmin'])
def manage_user():
    try:
        jumlah_user_terverifikasi = User.query.filter_by(is_verified=True).count()
        jumlah_user_belum_terverifikasi = User.query.filter_by(is_verified=False).count()
        # Mengambil semua data user dari database
        users = User.query.all()
        return render_template('admin/manage-user.html', users=users , time=time , jumlah_user_terverifikasi=jumlah_user_terverifikasi , jumlah_user_belum_terverifikasi=jumlah_user_belum_terverifikasi)
    except Exception as e:
        flash('Terjadi kesalahan saat memuat halaman manage user.', 'danger')
        return jsonify({'message': 'Error loading manage user', 'error': str(e)}), 500

@admin_blueprint.route('/article-post')
@login_required
@role_required(['superadmin'])
def article_post():
    try:
        # Mengambil semua data user dari database
        users = User.query.all()
        return render_template('admin/article-post-admin.html', users=users , time=time)
    except Exception as e:
        flash('Terjadi kesalahan saat memuat halaman article post.', 'danger')
        return jsonify({'message': 'Error loading manage user', 'error': str(e)}), 500


@admin_blueprint.route('/settings')
@login_required
@role_required(['admin', 'superadmin'])
def settings():
    # Pastikan user ada di session
    if 'user' not in session or 'email' not in session['user']:
        flash('Anda harus login terlebih dahulu.', 'danger')
        return redirect(url_for('auth.login'))

    # Ambil user berdasarkan email dari session
    user = User.query.filter_by(email=session['user']['email']).first()

    # Jika user tidak ditemukan
    if not user:
        flash('User tidak ditemukan. Silakan login kembali.', 'danger')
        return redirect(url_for('auth.login'))

    # Perbarui session dengan avatar fallback ke default jika tidak ada
    session['user'] = {
        "id": user.id,
        "nama_user": user.nama_user,
        "email": user.email,
        "nomor_hp": user.nomor_hp,
        "tanggal_lahir": user.tanggal_lahir,
        "jenis_kelamin": user.jenis_kelamin,
        "role": user.role,
        "avatar": user.avatar if user.avatar and os.path.exists(os.path.join('static/uploads/avatars', user.avatar)) else 'default-avatar.png',

    }

    # Tambahkan `time` untuk cache-busting pada gambar avatar
    return render_template('admin/settings-admin.html', user=user, time=time)


