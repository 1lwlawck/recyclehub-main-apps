from flask import Blueprint, jsonify, request ,render_template , session , redirect , url_for
from models.models import User  # Pastikan import model sesuai struktur Anda
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

@user_blueprint.route('/get-users', methods=['GET'])
def get_users():
    try:
        # Ambil parameter
        page = int(request.args.get('page', 1))  # Halaman saat ini
        limit = int(request.args.get('limit', 10))  # Jumlah data per halaman
        search = request.args.get('search', '')  # Input pencarian

        # Hitung offset
        offset = (page - 1) * limit

        # Query dengan filter pencarian
        query = User.query
        if search:
            query = query.filter(
                User.nama_user.ilike(f"%{search}%") | User.email.ilike(f"%{search}%")
            )

        # Query data dengan limit dan offset
        users = query.order_by(User.id).offset(offset).limit(limit).all()

        # Hitung total data (termasuk hasil filter)
        total_users = query.count()

        # Format data
        users_list = [{
            "id": user.id,
            "nama_user": user.nama_user,
            "email": user.email,
            "role": user.role,
            "is_verified": user.is_verified,
            "otp": user.otp
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


@user_blueprint.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'User tidak ditemukan'}), 404

        # Hapus data pengguna
        db.session.delete(user)
        db.session.commit()

        # Reset ID secara berurutan
        reset_ids()

        return jsonify({'success': True, 'message': 'User berhasil dihapus'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


def reset_ids():
    """Fungsi untuk mereset ID secara berurutan"""
    # Ambil semua data dengan urutan baru
    users = User.query.order_by(User.id).all()

    # Reset ID untuk setiap user
    for index, user in enumerate(users):
        user.id = index + 1

    # Update database
    db.session.commit()

    # Set auto increment ke ID terakhir
    db.session.execute(text("ALTER TABLE users AUTO_INCREMENT = :id"), {"id": len(users) + 1})
    db.session.commit()

@user_blueprint.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()

        # Validasi input
        if 'nama_user' in data and not data['nama_user'].strip():
            return jsonify({'success': False, 'message': 'Nama pengguna tidak boleh kosong'}), 400
        if 'email' in data and not data['email'].strip():
            return jsonify({'success': False, 'message': 'Email tidak boleh kosong'}), 400

        # Ambil user berdasarkan ID atau session
        if user_id == 0:
            user = User.query.filter_by(email=session['user']['email']).first()
        else:
            user = User.query.get(user_id)

        if not user:
            return jsonify({'success': False, 'message': 'User tidak ditemukan'}), 404

        # Update field yang diizinkan
        allowed_fields = ['nama_user', 'email']
        for field, value in data.items():
            if field in allowed_fields:
                setattr(user, field, value)

        db.session.commit()

        # Perbarui session jika user yang sedang login diperbarui
        if user_id == 0:
            session['user'] = {
                "id": user.id,
                "nama_user": user.nama_user,
                "email": user.email,
                "role": user.role,
                "avaatar": user.avatar or 'default-avatar.png'
            }

        return jsonify({'success': True, 'message': 'User berhasil diperbarui'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# Fungsi validasi ekstensi file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Upload avatar
@user_blueprint.route('/upload-avatar', methods=['POST'])
def upload_avatar():
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': 'Tidak ada file yang diunggah'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'success': False, 'message': 'File tidak dipilih'}), 400

    if file and allowed_file(file.filename):
        try:
            # Amankan nama file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Ambil user dari session
            user = User.query.filter_by(email=session['user']['email']).first()
            if not user:
                return jsonify({'success': False, 'message': 'User tidak ditemukan'}), 404

            # Hapus avatar lama jika ada dan bukan default
            if user.avatar and user.avatar != DEFAULT_AVATAR:
                old_avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], user.avatar)
                if os.path.exists(old_avatar_path):
                    os.remove(old_avatar_path)

            # Simpan avatar baru
            file.save(file_path)
            user.avatar = filename  # Update nama file avatar di database
            db.session.commit()

            # **Perbarui session**
            session['user']['avatar'] = user.avatar  # Update avatar di session

            # Kirim URL avatar baru
            avatar_url = url_for('static', filename=f'uploads/avatars/{filename}')
            return jsonify({'success': True, 'message': 'Avatar berhasil diperbarui', 'avatar_url': avatar_url})

        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    else:
        return jsonify({'success': False, 'message': 'Tipe file tidak diperbolehkan'}), 400



# Reset avatar ke default
@user_blueprint.route('/reset-avatar', methods=['POST'])
def reset_avatar():
    try:
        user = User.query.filter_by(email=session['user']['email']).first()
        if not user:
            return jsonify({'success': False, 'message': 'User tidak ditemukan'}), 404

        # Hapus avatar lama jika bukan default
        if user.avatar and user.avatar != DEFAULT_AVATAR:
            old_avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], user.avatar)
            if os.path.exists(old_avatar_path):
                os.remove(old_avatar_path)

        # Set avatar ke default
        user.avatar = DEFAULT_AVATAR
        db.session.commit()

        # **Perbarui session**
        session['user']['avatar'] = user.avatar  # Update avatar di session

        avatar_url = url_for('static', filename=f'uploads/avatars/{DEFAULT_AVATAR}')
        return jsonify({'success': True, 'message': 'Avatar berhasil direset', 'avatar_url': avatar_url})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
