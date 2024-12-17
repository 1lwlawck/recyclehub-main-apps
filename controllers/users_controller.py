from flask import Blueprint, jsonify, request, session, redirect, url_for, flash
from models.user import User
from models.points import Points
from app import db, app
from sqlalchemy.sql import text
from werkzeug.utils import secure_filename
import os
from time import time

user_blueprint = Blueprint('user', __name__, url_prefix='/user')

# Lokasi penyimpanan avatar
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads/avatars')
DEFAULT_AVATAR = 'default-avatar.png'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Fungsi validasi ekstensi file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# GET USERS - Ambil daftar user dengan pagination
@user_blueprint.route('/get-users', methods=['GET'])
def get_users():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        search = request.args.get('search', '')

        query = User.query
        if search:
            query = query.filter(User.nama_user.ilike(f"%{search}%") | User.email.ilike(f"%{search}%"))

        users = query.order_by(User.id).offset((page - 1) * limit).limit(limit).all()
        total_users = query.count()

        users_list = [{
            "id": user.id,
            "nama_user": user.nama_user,
            "email": user.email,
            "role": user.role,
            "is_verified": user.is_verified,
            "otp": user.otp,
            "points": Points.query.filter_by(user_id=user.id).first().points if Points.query.filter_by(user_id=user.id).first() else 0
        } for user in users]

        return jsonify({
            'success': True,
            'users': users_list,
            'total': total_users,
            'page': page,
            'limit': limit
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# DELETE USER
@user_blueprint.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'User tidak ditemukan'}), 404

        db.session.delete(user)
        db.session.commit()
        reset_ids()

        return jsonify({'success': True, 'message': 'User berhasil dihapus'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# Fungsi Reset ID
def reset_ids():
    users = User.query.order_by(User.id).all()
    for index, user in enumerate(users):
        user.id = index + 1
    db.session.commit()
    db.session.execute(text("ALTER TABLE users AUTO_INCREMENT = :id"), {"id": len(users) + 1})
    db.session.commit()

@user_blueprint.route('/update/<int:user_id>', methods=['POST'])
def update_user(user_id):
    try:
        print("=== Debugging: Mulai update_user ===")  # Debugging Start
        
        # 1. Ambil user berdasarkan ID
        user = User.query.get(user_id)
        if not user:
            print("User tidak ditemukan!")  # Debug
            flash("User tidak ditemukan.", "personal_profile_error")
            return redirect(url_for('admin.settings'))

        # 2. Validasi Input Nama dan Email
        nama_user = request.form.get('nama_user', '').strip()
        email = request.form.get('email', '').strip()
        print(f"Input Nama User: {nama_user}, Email: {email}")  # Debug

        if not nama_user or not email:
            print("Nama pengguna atau email kosong!")  # Debug
            flash("Nama pengguna dan email tidak boleh kosong.", "personal_profile_error")
            return redirect(url_for('admin.settings'))

        user.nama_user = nama_user
        user.email = email

        # 3. Handle Avatar Upload
        if 'avatar' in request.files:
            file = request.files['avatar']
            print("Avatar File Ditemukan:", file.filename)  # Debug

            if file and allowed_file(file.filename):
                print("Ekstensi File Diperbolehkan")  # Debug

                # Generate nama file unik
                filename = f"{int(time())}_{secure_filename(file.filename)}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                print("Filepath Avatar Baru:", filepath)  # Debug

                # Hapus avatar lama jika bukan default
                if user.avatar and user.avatar != DEFAULT_AVATAR:
                    old_avatar_path = os.path.join(UPLOAD_FOLDER, user.avatar)
                    if os.path.exists(old_avatar_path):
                        os.remove(old_avatar_path)
                        print("Avatar Lama Dihapus:", old_avatar_path)  # Debug

                # Simpan avatar baru
                file.save(filepath)
                print("Avatar Baru Disimpan:", filepath)  # Debug
                user.avatar = filename
            else:
                print("File tidak valid atau tipe file tidak diperbolehkan.")  # Debug
                flash("Tipe file tidak valid. Gunakan format JPG, PNG, atau GIF.", "personal_profile_error")
                return redirect(url_for('admin.settings'))
        else:
            print("Tidak ada file avatar yang diunggah.")  # Debug

        # 4. Commit perubahan ke database
        db.session.commit()
        print("Database diperbarui.")  # Debug

        # 5. Update session
        session['user'] = {
            'id': user.id,
            'nama_user': user.nama_user,
            'email': user.email,
            'avatar': user.avatar if user.avatar else DEFAULT_AVATAR,
            'role': user.role
        }
        print("Session diperbarui:", session['user'])  # Debug

        # 6. Flash message sukses
        flash("Profil berhasil diperbarui.", "personal_profile_success")
        print("=== Debugging: Selesai update_user ===")  # Debugging End
        return redirect(url_for('admin.settings'))

    except Exception as e:
        print("Error terjadi:", str(e))  # Debug
        flash(f"Terjadi kesalahan: {str(e)}", "personal_profile_error")
        return redirect(url_for('admin.settings'))

# RESET AVATAR KE DEFAULT
@user_blueprint.route('/reset-avatar', methods=['POST'])
def reset_avatar():
    try:
        user = User.query.filter_by(email=session['user']['email']).first()
        if not user:
            flash("User tidak ditemukan", "danger")
            return redirect(url_for('admin.settings'))

        # Hapus avatar lama jika bukan default
        if user.avatar and user.avatar != DEFAULT_AVATAR:
            old_avatar_path = os.path.join(UPLOAD_FOLDER, user.avatar)
            if os.path.exists(old_avatar_path):
                os.remove(old_avatar_path)

        user.avatar = DEFAULT_AVATAR
        db.session.commit()

        session['user']['avatar'] = DEFAULT_AVATAR
        flash("Avatar berhasil direset ke default", "success")
        return redirect(url_for('admin.settings'))
    except Exception as e:
        flash(f"Terjadi kesalahan: {str(e)}", "danger")
        return redirect(url_for('admin.settings'))
