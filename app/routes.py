from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import User
from sqlalchemy.exc import IntegrityError

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({
        'message': 'User Service API',
        'service': 'user-service',
        'status': 'running',
        'endpoints': {
            'POST /api/users': 'Create a new user',
            'GET /api/users': 'Get all users',
            'GET /api/users/<id>': 'Get user by ID',
            'GET /api/users/username/<username>': 'Get user by username',
            'PUT /api/users/<id>': 'Update user',
            'DELETE /api/users/<id>': 'Delete user'
        }
    })

@main.route('/health')
def health():
    # Check database connection
    try:
        db.session.execute(db.text('SELECT 1'))
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status
    }), 200

@main.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if username or email already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 409
        
        # Hash password
        password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        
        # Create user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=password_hash,
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database integrity error'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        users = User.query.all()
        return jsonify({
            'count': len(users),
            'users': [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/users/username/<username>', methods=['GET'])
def get_user_by_username(username):
    """Get user by username"""
    try:
        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'email' in data:
            # Check if email is taken by another user
            existing = User.query.filter_by(email=data['email']).first()
            if existing and existing.id != user_id:
                return jsonify({'error': 'Email already exists'}), 409
            user.email = data['email']
        
        if 'first_name' in data:
            user.first_name = data['first_name']
        
        if 'last_name' in data:
            user.last_name = data['last_name']
        
        if 'password' in data and data['password']:
            user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        
        if 'is_active' in data:
            user.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/users/verify', methods=['POST'])
def verify_password():
    """Verify user password (for authentication)"""
    try:
        data = request.get_json()
        
        if 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password required'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'User account is inactive'}), 401
        
        if bcrypt.check_password_hash(user.password_hash, data['password']):
            return jsonify({
                'message': 'Password verified',
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500