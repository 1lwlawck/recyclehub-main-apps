from flask import Blueprint, jsonify, request ,render_template
from models.models import User  # Pastikan import model sesuai struktur Anda
from app import db
from sqlalchemy.sql import text

user_blueprint = Blueprint('user', __name__, url_prefix='/user')


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
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'User tidak ditemukan'}), 404

        # Field yang diizinkan untuk diperbarui
        allowed_fields = ['nama_user', 'email', 'role']
        for field, value in data.items():
            if field in allowed_fields:
                setattr(user, field, value)

        db.session.commit()
        return jsonify({'success': True, 'message': 'User berhasil diperbarui'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

