from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe


class VerificationUtils:
    @staticmethod
    def generate_otp():
        return token_urlsafe(32)
    
    @staticmethod
    def create_expiry_date(expiry_minutes=10):
        return datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)
    
    @staticmethod
    def is_token_expired(expiry_datetime):
        return datetime.now(timezone.utc) > expiry_datetime