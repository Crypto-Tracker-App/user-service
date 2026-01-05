from flask import Blueprint, request, jsonify, g
import logging

from ..middleware.auth_middleware import auth_required
from ..services.auth_service import AuthService
from ..services.jwt_service import JWTService

logger = logging.getLogger(__name__)
auth_blueprint = Blueprint('api', __name__)

@auth_blueprint.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid request'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not all([username, password]):
        return jsonify({'error': 'All fields are required'}), 400
    
    result = AuthService.register_user(username, password)
    
    if 'error' in result:
        return jsonify({'error': result['error']}), result['status_code']
    return jsonify({'message': result['message']}), result['status_code']


@auth_blueprint.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Invalid request'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not all([username, password]):
            return jsonify({'error':'All fields required'}), 400
        
        result = AuthService.login_user(username, password)
        if 'error' in result: 
            return jsonify({'error': result['error']}), result['status_code']
        return jsonify({
            'token': result['token'],
            'user': result['user']
        }), result['status_code']
    except Exception as e:
        logger.error(f"Login endpoint error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal Server Error'}), 500


@auth_blueprint.route('/logout', methods=['POST'])
@auth_required
def logout():
    # With JWT, logout is handled client-side by removing the token
    return jsonify({'message':'Logged out successfully'}), 200


@auth_blueprint.route('/verify-session', methods=['GET'])
def verify_session():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
        user_data = JWTService.verify_token(token)
        
        if not user_data:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        return jsonify({
            'message': 'Token valid',
            'user': {
                'id': user_data['user_id'],
                'username': user_data['username']
            }
        }), 200
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        return jsonify({'error': 'Invalid token'}), 401

@auth_blueprint.route('/current-user', methods=['GET'])
@auth_required
def current_user():
    return jsonify({
        'user': {
            'id': g.current_user['user_id'],
            'username': g.current_user['username']
        }
    }), 200
    
