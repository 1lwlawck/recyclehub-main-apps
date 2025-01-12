from flask import Blueprint, request, jsonify
from app import db
from models.alamat import Alamat
from models.user import User
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.DEBUG)

# Blueprint untuk Alamat API
alamat_api = Blueprint('alamat_api', __name__, url_prefix='/api')

# 1. Buat alamat baru
@alamat_api.route('/alamat', methods=['POST'])
def create_alamat():
    try:
        data = request.get_json()
        required_fields = ['user_id', 'provinsi', 'kabupaten_kota', 'kecamatan', 'desa', 'alamat_lengkap']

        # Validasi data wajib
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400

        # Validasi user
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Membuat alamat baru
        alamat = Alamat(
            user_id=data['user_id'],
            provinsi=data['provinsi'],
            kabupaten_kota=data['kabupaten_kota'],
            kecamatan=data['kecamatan'],
            desa=data['desa'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            kode_pos=data.get('kode_pos'),
            alamat_lengkap=data['alamat_lengkap'],
        )
        db.session.add(alamat)
        db.session.commit()

        return jsonify({'message': 'Alamat created successfully', 'alamat_id': alamat.id}), 201

    except Exception as e:
        logging.error(f"Error creating address: {e}")
        return jsonify({'error': str(e)}), 500

# 2. Ambil semua alamat atau berdasarkan user_id
@alamat_api.route('/alamat', methods=['GET'])
def get_alamat():
    try:
        # Cek apakah ada parameter user_id
        user_id = request.args.get('user_id')

        if user_id:
            try:
                user_id = int(user_id)
            except ValueError:
                return jsonify({'error': 'Invalid user_id format'}), 400

            # Filter alamat berdasarkan user_id
            alamat_list = Alamat.query.filter(Alamat.user_id == user_id).all()
        else:
            # Ambil semua alamat jika tidak ada user_id
            alamat_list = Alamat.query.all()

        if not alamat_list:
            return jsonify([]), 200

        # Format data alamat ke JSON
        result = [
            {
                'id': alamat.id,
                'user_id': alamat.user_id,
                'provinsi': alamat.provinsi,
                'kabupaten_kota': alamat.kabupaten_kota,
                'kecamatan': alamat.kecamatan,
                'desa': alamat.desa,
                'latitude': alamat.latitude,
                'longitude': alamat.longitude,
                'kode_pos': alamat.kode_pos,
                'alamat_lengkap': alamat.alamat_lengkap,
            }
            for alamat in alamat_list
        ]

        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Error fetching addresses: {e}")
        return jsonify({'error': str(e)}), 500

# 3. Ambil alamat berdasarkan ID
@alamat_api.route('/alamat/<int:id>', methods=['GET'])
def get_alamat_by_id(id):
    try:
        alamat = Alamat.query.get(id)
        if not alamat:
            return jsonify({'error': 'Alamat not found'}), 404

        return jsonify({
            'id': alamat.id,
            'user_id': alamat.user_id,
            'provinsi': alamat.provinsi,
            'kabupaten_kota': alamat.kabupaten_kota,
            'kecamatan': alamat.kecamatan,
            'desa': alamat.desa,
            'latitude': alamat.latitude,
            'longitude': alamat.longitude,
            'kode_pos': alamat.kode_pos,
            'alamat_lengkap': alamat.alamat_lengkap
        }), 200

    except Exception as e:
        logging.error(f"Error fetching address by ID: {e}")
        return jsonify({'error': str(e)}), 500

# 4. Hapus alamat berdasarkan ID
@alamat_api.route('/alamat/<int:id>', methods=['DELETE'])
def delete_alamat(id):
    try:
        alamat = Alamat.query.get(id)
        if not alamat:
            return jsonify({'error': 'Alamat not found'}), 404

        db.session.delete(alamat)
        db.session.commit()

        return jsonify({'message': 'Alamat deleted successfully'}), 200

    except Exception as e:
        logging.error(f"Error deleting address: {e}")
        return jsonify({'error': str(e)}), 500

# 5. Perbarui alamat berdasarkan ID
@alamat_api.route('/alamat/<int:id>', methods=['PUT'])
def update_alamat(id):
    try:
        data = request.get_json()
        alamat = Alamat.query.get(id)
        if not alamat:
            return jsonify({'error': 'Alamat not found'}), 404

        updatable_fields = ['provinsi', 'kabupaten_kota', 'kecamatan', 'desa', 'latitude', 'longitude', 'kode_pos', 'alamat_lengkap']
        for field in updatable_fields:
            if field in data:
                setattr(alamat, field, data[field])

        db.session.commit()

        return jsonify({'message': 'Alamat updated successfully'}), 200

    except Exception as e:
        logging.error(f"Error updating address: {e}")
        return jsonify({'error': str(e)}), 500
