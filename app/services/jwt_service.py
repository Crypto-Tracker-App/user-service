import jwt
import os
from datetime import datetime, timedelta, timezone
import logging

logger = logging.getLogger(__name__)

class JWTService:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM = "HS256"
    EXPIRATION_MINUTES = 60 * 24  # 24 hours
    
    @staticmethod
    def create_token(user_id: int, username: str) -> str:
        """Create a JWT token for a user."""
        try:
            payload = {
                'user_id': user_id,
                'username': username,
                'iat': datetime.now(timezone.utc),
                'exp': datetime.now(timezone.utc) + timedelta(minutes=JWTService.EXPIRATION_MINUTES)
            }
            token = jwt.encode(payload, JWTService.SECRET_KEY, algorithm=JWTService.ALGORITHM)
            return token
        except Exception as e:
            logger.error(f"Token creation error: {str(e)}", exc_info=True)
            raise
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, JWTService.SECRET_KEY, algorithms=[JWTService.ALGORITHM])
            return {
                'user_id': payload.get('user_id'),
                'username': payload.get('username')
            }
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            return None
        except jwt.InvalidTokenError:
            logger.error("Invalid token")
            return None
        except Exception as e:
            logger.error(f"Token verification error: {str(e)}", exc_info=True)
            return None
