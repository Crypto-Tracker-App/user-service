from flask import Blueprint, request, jsonify, g
import logging

from ..middleware.auth_middleware import auth_required
from ..services.auth_service import AuthService
from ..services.jwt_service import JWTService

logger = logging.getLogger(__name__)
auth_blueprint = Blueprint('api', __name__)

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
    """
    Logout the current user. Handeled by frontend by deleting the token.
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
    # With JWT, logout is handled client-side by removing the token
    return jsonify({'message':'Logged out successfully'}), 200


@auth_blueprint.route('/verify-session', methods=['GET'])
def verify_session():
    """
    Verify if the current login session is valid
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
