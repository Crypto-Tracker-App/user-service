from flask import Blueprint, request, jsonify, g

from ..middleware.auth_middleware import auth_required
from ..services.auth_service import AuthService
from ..services.session_service import SessionService

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=["POST"])
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: Username for the new account
            password:
              type: string
              description: Password for the new account
    responses:
      201:
        description: User registered successfully
        schema:
          type: object
          properties:
            message:
              type: string
      400:
        description: Invalid request or missing fields
        schema:
          type: object
          properties:
            error:
              type: string
      409:
        description: User already exists
        schema:
          type: object
          properties:
            error:
              type: string
    """
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
    """
    Login user with username and password
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: User's username
            password:
              type: string
              description: User's password
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            user:
              type: object
              properties:
                id:
                  type: integer
                username:
                  type: string
      400:
        description: Invalid request or missing fields
        schema:
          type: object
          properties:
            error:
              type: string
      401:
        description: Invalid credentials
        schema:
          type: object
          properties:
            error:
              type: string
    """
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
    """
    Logout the current user
    ---
    tags:
      - Authentication
    security:
      - SessionAuth: []
    responses:
      200:
        description: User logged out successfully
        schema:
          type: object
          properties:
            message:
              type: string
      401:
        description: Unauthorized - session invalid or expired
        schema:
          type: object
          properties:
            error:
              type: string
    """
    SessionService.clear_session()
    return jsonify({'message':'Logged out successfully'}), 200


@auth_blueprint.route('/verify-session', methods=['GET'])
@auth_required
def verify_session():
    """
    Verify if the current session is valid
    ---
    tags:
      - Authentication
    security:
      - SessionAuth: []
    responses:
      200:
        description: Session is valid
        schema:
          type: object
          properties:
            message:
              type: string
            user:
              type: object
              properties:
                id:
                  type: integer
                username:
                  type: string
      401:
        description: Unauthorized - session invalid or expired
        schema:
          type: object
          properties:
            error:
              type: string
    """
    return jsonify({
        'message':'Session valid',
        'user': {'id': g.current_user['user_id'],
                 'username': g.current_user['username']
            }
        }), 200

@auth_blueprint.route('/current-user', methods=['GET'])
@auth_required
def current_user():
    """
    Get the current user information
    ---
    tags:
      - Authentication
    security:
      - SessionAuth: []
    responses:
      200:
        description: Current user information retrieved successfully
        schema:
          type: object
          properties:
            user:
              type: object
              properties:
                id:
                  type: integer
                username:
                  type: string
      401:
        description: Unauthorized - session invalid or expired
        schema:
          type: object
          properties:
            error:
              type: string
    """
    return jsonify({
        'user': {
            'id': g.current_user['user_id'],
            'username': g.current_user['username']
        }
    }), 200
