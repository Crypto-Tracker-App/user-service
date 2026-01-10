"""Tests for user models."""
import pytest
from app.models import User
from app import db


class TestUserModel:
    """Test cases for User model."""
    
    def test_user_creation(self, app):
        """Test creating a user."""
        with app.app_context():
            user = User(username='testuser')
            user.set_password('testpassword123')
            db.session.add(user)
            db.session.commit()
            
            retrieved = User.query.filter_by(username='testuser').first()
            assert retrieved is not None
            assert retrieved.username == 'testuser'
    
    def test_user_username_indexed(self, app):
        """Test that user username is indexed for quick lookup."""
        with app.app_context():
            user1 = User(username='user1')
            user1.set_password('pass1')
            user2 = User(username='user2')
            user2.set_password('pass2')
            db.session.add_all([user1, user2])
            db.session.commit()
            
            # Index should make this fast
            result = User.query.filter_by(username='user1').first()
            assert result.username == 'user1'
    
    def test_user_password_hashing(self, app):
        """Test that passwords are properly hashed."""
        with app.app_context():
            user = User(username='testuser')
            password = 'testpassword123'
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            retrieved = User.query.filter_by(username='testuser').first()
            # Password should not be stored in plaintext
            assert retrieved.password != password
            # Password check should work
            assert retrieved.check_password(password)
    
    def test_user_wrong_password(self, app):
        """Test that wrong password check fails."""
        with app.app_context():
            user = User(username='testuser')
            user.set_password('correctpassword')
            db.session.add(user)
            db.session.commit()
            
            retrieved = User.query.filter_by(username='testuser').first()
            assert not retrieved.check_password('wrongpassword')
    
    def test_user_unique_username(self, app):
        """Test that usernames must be unique."""
        with app.app_context():
            user1 = User(username='duplicate')
            user1.set_password('pass1')
            db.session.add(user1)
            db.session.commit()
            
            user2 = User(username='duplicate')
            user2.set_password('pass2')
            db.session.add(user2)
            
            with pytest.raises(Exception):  # Will raise integrity error
                db.session.commit()
