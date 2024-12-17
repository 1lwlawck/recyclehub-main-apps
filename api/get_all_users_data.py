from flask import Blueprint, jsonify , request
from models.user import User
from models.points import Points
from app import db

# Inisialisasi Blueprint
get_all_users_bp = Blueprint('get_all_users', __name__ , url_prefix='/api/users')

# API GET ALL USERS (Semua user atau berdasarkan ID)
@get_all_users_bp.route('/get-all-users', methods=['GET'])
def get_all_users():
    try:
        # Ambil parameter ID (opsional)
        user_id = request.args.get('id', type=int)  # Ambil ID dari query parameter

        if user_id:  # Jika ID diberikan
            # Query data user berdasarkan ID
            user = User.query.get(user_id)
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'User tidak ditemukan.'
                }), 404

            # Format hasil query menjadi JSON
            user_data = {
                "id": user.id,
                "nama_user": user.nama_user,
                "email": user.email,
                "role": user.role,
                "is_verified": user.is_verified,
                "otp": user.otp,
                "nomor_hp": user.nomor_hp,
                "tanggal_lahir": user.tanggal_lahir.strftime("%Y-%m-%d") if user.tanggal_lahir else None,
                "jenis_kelamin": user.jenis_kelamin,
                "avatar": user.avatar,
                "points": Points.query.filter_by(user_id=user.id).first().points if Points.query.filter_by(user_id=user.id).first() else 0
            }

            # Kembalikan data user tunggal
            return jsonify({
                'success': True,
                'user': user_data
            }), 200
        else:  # Jika tidak ada ID, ambil semua user
            users = User.query.order_by(User.id).all()

            # Format semua data user menjadi JSON
            users_list = [{
                "id": user.id,
                "nama_user": user.nama_user,
                "email": user.email,
                "role": user.role,
                "is_verified": user.is_verified,
                "otp": user.otp,
                "nomor_hp": user.nomor_hp,
                "tanggal_lahir": user.tanggal_lahir.strftime("%Y-%m-%d") if user.tanggal_lahir else None,
                "jenis_kelamin": user.jenis_kelamin,
                "avatar": user.avatar,
                "points": Points.query.filter_by(user_id=user.id).first().points if Points.query.filter_by(user_id=user.id).first() else 0
            } for user in users]

            # Kembalikan data semua user
            return jsonify({
                'success': True,
                'users': users_list,
                'total_users': len(users_list)
            }), 200

    except Exception as e:
        # Tangani error jika terjadi
        return jsonify({
            'success': False,
            'message': f"Terjadi kesalahan: {str(e)}"
        }), 500
