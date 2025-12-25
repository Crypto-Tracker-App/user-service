from ..extensions import db
from ..models import User
from .session_service import SessionService


class AuthService:
    @staticmethod
    def register_user(username: str, password: str):
        try:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return {"error": "User already exists", "status_code": 400}

            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            return {
                "message": "Registration successful! Please check your email to verify your account.",
                "status_code": 201
            }
        except Exception:
            db.session.rollback()
            return {"error": "Internal Server Error", "status_code": 500}

    @staticmethod
    def login_user(username: str, password: str):
        try:
            user = User.query.filter_by(username=username).first()
            if not user:
                return {"error": "User does not exist", "status_code": 403}
            
            password_valid = user.check_password(password)
            if not password_valid:
                return {"error": "Invalid credentials", "status_code": 403}
            SessionService.create_session(user.id, user.username)
            return {
                "message": "Login successful",
                "user": {"id": user.id, "username": user.username},
                "status_code": 200
            }
        except Exception:
            return {"error": "Internal Server Error", "status_code": 500}