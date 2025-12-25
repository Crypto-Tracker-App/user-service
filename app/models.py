from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, String, DateTime

import uuid
from datetime import datetime, timezone

from .extensions import db

def generate_unique_id():
    return str(uuid.uuid4())

class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True, default=generate_unique_id)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)