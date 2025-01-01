from flask import Blueprint, jsonify, request
from models.user import User
from models.points import Points
from utils import get_user_by_id, delete_old_avatar, save_new_avatar
from app import db
from datetime import datetime

users_api_blueprint = Blueprint("users_api", __name__, url_prefix="/api/users")

@users_api_blueprint.route('/get-users', methods=['GET'])
def get_users():
    try:
        user_id = request.args.get('id', type=int)
        if user_id:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'success': False, 'message': 'User tidak ditemukan'}), 404

            points = Points.query.filter_by(user_id=user.id).first()
            return jsonify({
                'success': True,
                'user': {
                    'id': user.id,
                    'nama_user': user.nama_user,
                    'email': user.email,
                    'role': user.role,
                    'is_verified': user.is_verified,
                    'otp': user.otp,
                    'nomor_hp': user.nomor_hp,
                    'tanggal_lahir': user.tanggal_lahir.strftime('%Y-%m-%d') if user.tanggal_lahir else None,
                    'jenis_kelamin': user.jenis_kelamin,
                    'points': points.points if points else 0,
                },
            }), 200

        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        search = request.args.get('search', '', type=str).strip()

        query = User.query
        if search:
            query = query.filter(User.nama_user.ilike(f"%{search}%") | User.email.ilike(f"%{search}%"))

        total_users = query.count()
        users = query.order_by(User.id).offset((page - 1) * limit).limit(limit).all()
        user_ids = [user.id for user in users]
        points = {point.user_id: point.points for point in Points.query.filter(Points.user_id.in_(user_ids)).all()}

        users_list = [
            {
                "id": user.id,
                "nama_user": user.nama_user,
                "email": user.email,
                "role": user.role,
                "is_verified": user.is_verified,
                "otp": user.otp,
                "nomor_hp": user.nomor_hp,
                'tanggal_lahir': user.tanggal_lahir.strftime('%Y-%m-%d') if user.tanggal_lahir else None,
                "jenis_kelamin": user.jenis_kelamin,
                "points": points.get(user.id, 0),
            }
            for user in users
        ]

        return jsonify({"success": True, "users": users_list, "total": total_users, "page": page, "limit": limit}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': 'Terjadi kesalahan pada server'}), 500


@users_api_blueprint.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        # Ambil user berdasarkan ID
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'User tidak ditemukan'}), 404

        # Hapus data terkait di tabel points (jika ada)
        db.session.query(Points).filter_by(user_id=user_id).delete()

        # Hapus avatar jika bukan default
        delete_old_avatar(user)

        # Hapus user dari tabel users
        db.session.delete(user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'User berhasil dihapus'}), 200
    except Exception as e:
        db.session.rollback()  # Rollback transaksi jika terjadi kesalahan
        return jsonify({'success': False, 'message': f'Gagal menghapus user: {str(e)}'}), 500

@users_api_blueprint.route('/update/<int:user_id>', methods=['PUT'])
def update_user_api(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"success": False, "message": "User tidak ditemukan"}), 404

        # Ambil data dari JSON request
        data = request.json
        nama_user = data.get('nama_user', '').strip()
        email = data.get('email', '').strip()
        nomor_hp = data.get('nomor_hp', '').strip()
        jenis_kelamin = data.get('jenis_kelamin', '').strip()
        tanggal_lahir = data.get('tanggal_lahir', '').strip()

        # Validasi nama dan email
        if not nama_user or not email:
            return jsonify({"success": False, "message": "Nama dan email tidak boleh kosong"}), 400

        # Validasi nomor HP
        if not nomor_hp.isdigit():
            return jsonify({"success": False, "message": "Nomor HP harus berupa angka"}), 400

        # Validasi jenis kelamin
        if jenis_kelamin not in ['Laki-laki', 'Perempuan']:
            return jsonify({"success": False, "message": "Jenis kelamin tidak valid"}), 400

        # Validasi tanggal lahir
        try:
            tanggal_lahir = datetime.strptime(tanggal_lahir, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"success": False, "message": "Tanggal lahir tidak valid"}), 400

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
                return jsonify({"success": False, "message": "Tipe file avatar tidak valid"}), 400

        # Commit perubahan ke database
        db.session.commit()

        return jsonify({"success": True, "message": "Profil berhasil diperbarui"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Terjadi kesalahan: {str(e)}"}), 500

@users_api_blueprint.route('/edit-user/<int:user_id>', methods=['PUT'])
def edit_user_from_table(user_id):
    try:
        # Cari user berdasarkan ID
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'User tidak ditemukan'}), 404

        # Ambil data dari request body
        data = request.get_json()
        nama_user = data.get('nama_user', '').strip()
        email = data.get('email', '').strip()
        role = data.get('role', '').strip()
        points = data.get('points')
        nomor_hp = data.get('nomor_hp', '').strip()
        tanggal_lahir = data.get('tanggal_lahir', '').strip()
        jenis_kelamin = data.get('jenis_kelamin', '').strip()

        # Validasi data
        if not nama_user or not email or not role or points is None:
            return jsonify({
                'success': False,
                'message': 'Nama, email, role, dan points tidak boleh kosong'
            }), 400

        if not nomor_hp.isdigit():
            return jsonify({'success': False, 'message': 'Nomor HP harus berupa angka'}), 400

        if not tanggal_lahir:
            return jsonify({'success': False, 'message': 'Tanggal lahir tidak boleh kosong'}), 400

        if jenis_kelamin not in ['Laki-laki', 'Perempuan']:
            return jsonify({'success': False, 'message': 'Jenis kelamin tidak valid'}), 400

        # Perbarui data user
        user.nama_user = nama_user
        user.email = email
        user.role = role
        user.nomor_hp = nomor_hp
        user.tanggal_lahir = tanggal_lahir
        user.jenis_kelamin = jenis_kelamin

        # Perbarui atau tambahkan points
        user_points = Points.query.filter_by(user_id=user_id).first()
        if user_points:
            user_points.points = points
        else:
            user_points = Points(user_id=user_id, points=points)
            db.session.add(user_points)

        # Simpan perubahan ke database
        db.session.commit()

        return jsonify({'success': True, 'message': 'User berhasil diperbarui'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


