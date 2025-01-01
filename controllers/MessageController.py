from flask import Blueprint, jsonify, request, session
from models.message import Message
from models.user import User
from app import db
from datetime import datetime

message_blueprint = Blueprint("message", __name__, url_prefix="/message")


@message_blueprint.route('/send', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        content = data.get('message')

        if not sender_id or not receiver_id or not content:
            return jsonify({'success': False, 'message': 'Sender, receiver, dan pesan tidak boleh kosong'}), 400

        sender = User.query.get(sender_id)
        receiver = User.query.get(receiver_id)

        if not sender or not receiver:
            return jsonify({'success': False, 'message': 'Pengirim atau penerima tidak ditemukan'}), 404

        # Simpan pesan ke database
        new_message = Message(sender_id=sender_id, receiver_id=receiver_id, message=content, timestamp=datetime.utcnow())
        db.session.add(new_message)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Pesan berhasil dikirim'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Terjadi kesalahan: {str(e)}'}), 500


@message_blueprint.route('/fetch/<int:receiver_id>', methods=['GET'])
def fetch_messages(receiver_id):
    try:
        sender_id = session.get('user_id')  # Pastikan Anda menyimpan `user_id` di session

        if not sender_id:
            return jsonify({'success': False, 'message': 'Pengguna belum login'}), 401

        messages = Message.query.filter(
            ((Message.sender_id == sender_id) & (Message.receiver_id == receiver_id)) |
            ((Message.sender_id == receiver_id) & (Message.receiver_id == sender_id))
        ).order_by(Message.timestamp.asc()).all()

        message_list = [{
            "id": message.id,
            "sender_id": message.sender_id,
            "receiver_id": message.receiver_id,
            "message": message.message,
            "timestamp": message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for message in messages]

        return jsonify({'success': True, 'messages': message_list}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Terjadi kesalahan: {str(e)}'}), 500


@message_blueprint.route('/delete/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    try:
        message = Message.query.get(message_id)

        if not message:
            return jsonify({'success': False, 'message': 'Pesan tidak ditemukan'}), 404

        db.session.delete(message)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Pesan berhasil dihapus'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Gagal menghapus pesan: {str(e)}'}), 500

