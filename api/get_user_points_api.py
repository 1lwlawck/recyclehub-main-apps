from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.points import Points
from models.user import User

points_blueprint = Blueprint('points', __name__, url_prefix='/api/points')

@points_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_user_points():
    try:
        # Ambil user_id dari access token
        user_id = get_jwt_identity()
        user_points = Points.query.filter_by(user_id=user_id).first()

        if not user_points:
            return jsonify({
                'success': False,
                'message': 'No points found for this user'
            }), 404

        return jsonify({
            'success': True,
            'user_id': user_id,
            'points': user_points.points
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching points',
            'error': str(e)
        }), 500

@points_blueprint.route('/all', methods=['GET'])
def get_all_user_points():
    try:
        # Ambil semua data poin
        all_points = Points.query.all()
        points_list = [{
            'user_id': point.user_id,
            'points': point.points,
            'created_at': point.created_at,
            'updated_at': point.updated_at
        } for point in all_points]

        return jsonify({
            'success': True,
            'points': points_list
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'An error occurred while fetching all user points.',
            'error': str(e)
        }), 500
