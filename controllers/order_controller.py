from flask import Blueprint, request, jsonify
from app import db
from models.order import Order, DetailSampah, JenisSampah

# Inisialisasi Blueprint
order_blueprint = Blueprint('order', __name__)


@order_blueprint.route('/orders', methods=['GET'])
def get_orders():
    """
    Endpoint untuk mendapatkan daftar order dengan pagination dan error handling.
    """
    try:
        # Ambil parameter pagination dari query string
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # Query data dengan pagination
        orders_paginated = Order.query.paginate(page=page, per_page=per_page, error_out=False)

        # Format data menjadi JSON
        response = {
            'total': orders_paginated.total,
            'page': orders_paginated.page,
            'per_page': orders_paginated.per_page,
            'data': [
                {
                    'id_order': order.id_order,
                    'id_user': order.id_user,
                    'tanggal_pengantaran': order.tanggal_pengantaran.isoformat(),
                    'waktu_pengantaran': str(order.waktu_pengantaran),
                    'status_order': order.status_order,
                    'details': [
                        {
                            'id_detail': detail.id_detail,
                            'jenis_sampah': detail.jenis_sampah.nama_jenis_sampah,
                            'perkiraan_berat': detail.perkiraan_berat,
                            'foto_sampah': detail.foto_sampah
                        } for detail in order.details
                    ]
                } for order in orders_paginated.items
            ]
        }

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch orders", "details": str(e)}), 500


@order_blueprint.route('/jenis_sampah', methods=['GET'])
def get_jenis_sampah():
    """
    Endpoint untuk mendapatkan daftar jenis sampah.
    """
    try:
        jenis_sampah = JenisSampah.query.all()
        return jsonify([
            {
                'id_jenis_sampah': jenis.id_jenis_sampah,
                'nama_jenis_sampah': jenis.nama_jenis_sampah
            } for jenis in jenis_sampah
        ]), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch jenis sampah", "details": str(e)}), 500


@order_blueprint.route('/jenis_sampah', methods=['POST'])
def add_jenis_sampah():
    """
    Endpoint untuk menambahkan jenis sampah baru.
    """
    try:
        data = request.json

        # Validasi input
        if not data or not data.get('nama_jenis_sampah'):
            return jsonify({"error": "Field 'nama_jenis_sampah' is required."}), 400

        # Tambahkan jenis sampah ke database
        new_jenis = JenisSampah(nama_jenis_sampah=data['nama_jenis_sampah'])
        db.session.add(new_jenis)
        db.session.commit()

        return jsonify({"message": "Jenis Sampah added successfully!", "id_jenis_sampah": new_jenis.id_jenis_sampah}), 201
    except Exception as e:
        return jsonify({"error": "Failed to add jenis sampah", "details": str(e)}), 500
