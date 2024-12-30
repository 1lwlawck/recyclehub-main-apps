from flask import Blueprint, jsonify, request
from models.message import Message
from models.user import User
from app import db

messages_api_blueprint = Blueprint("messages_api", __name__, url_prefix="/api/messages")


@messages_api_blueprint.route('/get-messages', methods=['GET'])
def get_messages():
    try:
        sender_id = request.args.get('sender_id', type=int)
        receiver_id = request.args.get('receiver_id', type=int)

        if not sender_id or not receiver_id:
            return jsonify({'success': False, 'message': 'Sender ID dan Receiver ID harus disediakan'}), 400

        # Ambil pesan berdasarkan sender dan receiver
        messages = Message.query.filter_by(sender_id=sender_id, receiver_id=receiver_id).order_by(Message.timestamp.asc()).all()
        messages_list = [
            {
                "id": message.id,
                "sender_id": message.sender_id,
                "receiver_id": message.receiver_id,
                "message": message.message,
                "timestamp": message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                "is_read": message.is_read
            }
            for message in messages
        ]

        return jsonify({'success': True, 'messages': messages_list}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': f'Terjadi kesalahan pada server: {str(e)}'}), 500


@messages_api_blueprint.route('/add-message', methods=['POST'])
def add_message():
    try:
        data = request.get_json()
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        message_content = data.get('message')

        if not sender_id or not receiver_id or not message_content:
            return jsonify({'success': False, 'message': 'Sender ID, Receiver ID, dan pesan tidak boleh kosong'}), 400

        # Validasi apakah pengguna ada
        sender = User.query.get(sender_id)
        receiver = User.query.get(receiver_id)
        if not sender or not receiver:
            return jsonify({'success': False, 'message': 'Pengirim atau penerima tidak ditemukan'}), 404

        # Tambahkan pesan ke database
        new_message = Message(sender_id=sender_id, receiver_id=receiver_id, message=message_content)
        db.session.add(new_message)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Pesan berhasil ditambahkan'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Gagal menambahkan pesan: {str(e)}'}), 500


@messages_api_blueprint.route('/delete-message/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    try:
        # Ambil pesan berdasarkan ID
        message = Message.query.get(message_id)
        if not message:
            return jsonify({'success': False, 'message': 'Pesan tidak ditemukan'}), 404

        # Hapus pesan
        db.session.delete(message)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Pesan berhasil dihapus'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Gagal menghapus pesan: {str(e)}'}), 500


@messages_api_blueprint.route('/get-user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        # Ambil data pengguna berdasarkan ID
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'Pengguna tidak ditemukan'}), 404

        # Kirim data pengguna
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'nama_user': user.nama_user,
                'avatar': user.avatar or "https://via.placeholder.com/40",  # Avatar default jika tidak tersedia
                'is_online': False  # Ini contoh, Anda bisa mengganti logika untuk status online
            }
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@messages_api_blueprint.route('/search-users', methods=['GET'])
def search_users():
    try:
        query = request.args.get('query', '').strip().lower()
        if not query:
            return jsonify({'success': True, 'users': []}), 200

        users = User.query.filter(User.nama_user.ilike(f"%{query}%")).all()
        users_list = [
            {
                "id": user.id,
                "nama_user": user.nama_user,
                "avatar": user.avatar or "https://via.placeholder.com/40"
            }
            for user in users
        ]

        return jsonify({'success': True, 'users': users_list}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500
