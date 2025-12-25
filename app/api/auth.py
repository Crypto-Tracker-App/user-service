from flask import Blueprint, request, jsonify, g

from ..middleware.auth_middleware import auth_required
from ..services.auth_service import AuthService
from ..services.session_service import SessionService

auth_blueprint = Blueprint('auth', __name__)

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
    return jsonify({'user':result['user']}), result['status_code']


@auth_blueprint.route('/logout', methods=['POST'])
@auth_required
def logout():
    SessionService.clear_session()
    return jsonify({'message':'Logged out successfully'}), 200


@auth_blueprint.route('/verify-session', methods=['GET'])
@auth_required
def verify_session():
    return jsonify({
        'message':'Session valid',
        'user': {'id': g.current_user['user_id'],
                 'username': g.current_user['username']
            }
        }), 200