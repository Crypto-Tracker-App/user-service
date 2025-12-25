from flask import session

from datetime import datetime, timezone

class SessionService:
    @staticmethod
    def create_session(user_id: str, username: str):
        session.permanent = True
        session['user_id'] = user_id
        session['username'] = username
        session['logged_in'] = True
        session['login_time'] = datetime.now(timezone.utc)
        
    @staticmethod
    def clear_session():
        session.clear()
    
    @staticmethod 
    def verify_session():
        try:
            if not session.get('logged_in'):
                return {'error':'Not authenticated'}
            user_id = session.get('user_id')
            username = session.get('username')
            
            if not user_id or not username:
                return {'error': 'Invalid session data'}
            
            return {
                'user_id' : user_id,
                'username' : username, 
                'login_time' : session.get('login_time')
            }
        except Exception as e:
            return {'error': 'Session verification failed'}
    
    @staticmethod
    def get_current_user_id():
        return session.get('user_id')
    
    @staticmethod
    def get_current_user_username():
        return session.get('username')