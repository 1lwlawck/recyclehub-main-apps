from flask import Blueprint, session, redirect, url_for, flash, request
from utils import get_user_by_id, delete_old_avatar, save_new_avatar, update_user_session
from app import db
from datetime import datetime

user_blueprint = Blueprint("user", __name__, url_prefix="/user")

@user_blueprint.route('/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    try:
        user = get_user_by_id(user_id)
        if not user:
            return redirect(url_for('admin.settings'))

        # Perbarui nama, email, nomor HP, jenis kelamin, dan tanggal lahir
        nama_user = request.form.get('nama_user', '').strip()
        email = request.form.get('email', '').strip()
        nomor_hp = request.form.get('nomor_hp', '').strip()
        jenis_kelamin = request.form.get('jenis_kelamin', '').strip()
        tanggal_lahir = request.form.get('tanggal_lahir', '').strip()

        # Validasi nama dan email
        if not nama_user or not email:
            flash("Nama pengguna dan email tidak boleh kosong.", "personal_profile_error")
            return redirect(url_for('admin.settings'))

        # Validasi nomor HP
        if not nomor_hp.isdigit():
            flash("Nomor HP harus berupa angka.", "personal_profile_error")
            return redirect(url_for('admin.settings'))

        # Validasi jenis kelamin
        if jenis_kelamin not in ['Laki-laki', 'Perempuan']:
            flash("Jenis kelamin tidak valid.", "personal_profile_error")
            return redirect(url_for('admin.settings'))

        # Validasi tanggal lahir
        try:
            tanggal_lahir = datetime.strptime(tanggal_lahir, '%Y-%m-%d').date()
        except ValueError:
            flash("Tanggal lahir tidak valid.", "personal_profile_error")
            return redirect(url_for('admin.settings'))

        # Perbarui data user
        user.nama_user = nama_user
        user.email = email
        user.nomor_hp = nomor_hp
        user.jenis_kelamin = jenis_kelamin
        user.tanggal_lahir = tanggal_lahir

        # Handle Avatar Upload
        if 'avatar' in request.files and request.files['avatar'].filename != '':
            file = request.files['avatar']
            if file:
                delete_old_avatar(user)
                user.avatar = save_new_avatar(file)
            else:
                flash("Tipe file tidak valid. Gunakan format JPG, PNG, atau GIF.", "personal_profile_error")
                return redirect(url_for('admin.settings'))

        db.session.commit()
        update_user_session(user)
        flash("Profil berhasil diperbarui.", "personal_profile_success")
        return redirect(url_for('admin.settings'))

    except Exception as e:
        flash(f"Terjadi kesalahan: {str(e)}", "personal_profile_error")
        return redirect(url_for('admin.settings'))



@user_blueprint.route('/reset-avatar', methods=['POST'])
def reset_avatar():
    try:
        user = User.query.filter_by(email=session['user']['email']).first()
        if not user:
            flash("User tidak ditemukan", "danger")
            return redirect(url_for('admin.settings'))

        delete_old_avatar(user)
        user.avatar = 'default-avatar.png'
        db.session.commit()

        update_user_session(user)
        flash("Avatar berhasil direset ke default", "success")
        return redirect(url_for('admin.settings'))
    except Exception as e:
        flash(f"Terjadi kesalahan: {str(e)}", "danger")
        return redirect(url_for('admin.settings'))
