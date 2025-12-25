from flask import jsonify, g
from functools import wraps

from ..services.session_service import SessionService

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        session_data = SessionService.verify_session()
        
        if 'error' in session_data:
            return jsonify({'error':'Authentication required'}), 401
        
        g.current_user = {
            'user_id' : session_data['user_id'], 
            'username' : session_data['username']
        }
        
        return f(*args, **kwargs)
    return decorated