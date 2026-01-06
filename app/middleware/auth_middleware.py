from flask import jsonify, g, request
from functools import wraps
import logging


from ..services.jwt_service import JWTService

logger = logging.getLogger(__name__)

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Authorization required'}), 401
        
        try:
            token = auth_header.split(' ')[1] if ' ' in auth_header else auth_header
            user_data = JWTService.verify_token(token)
            
            if not user_data:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            g.current_user = {
                'user_id': user_data['user_id'],
                'username': user_data['username']
            }
            
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Auth middleware error: {str(e)}")
            return jsonify({'error': 'Authentication failed'}), 401
    return decorated