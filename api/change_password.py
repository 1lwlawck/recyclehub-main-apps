from flask import Blueprint, request, jsonify
from models.models import User
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from utils import login_required

@password_api_blueprint.route('/change', methods=['POST'])
@login_required
def change_password():
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    if not current_password or not new_password or not confirm_password:
        return jsonify({'success': False, 'message': 'Semua field wajib diisi.'}), 400

    # Ambil user dari session (atau JWT token jika digunakan)
    user = User.query.filter_by(email=session['user']['email']).first()
    if not user:
        return jsonify({'success': False, 'message': 'User tidak ditemukan.'}), 404

    # Validasi password lama
    if not check_password_hash(user.password_hash, current_password):
        return jsonify({'success': False, 'message': 'Password lama salah.'}), 400

    # Validasi password baru dan konfirmasi
    if new_password != confirm_password:
        return jsonify({'success': False, 'message': 'Password baru dan konfirmasi tidak cocok.'}), 400

    # Update password
    user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Password berhasil diubah.'}), 200
