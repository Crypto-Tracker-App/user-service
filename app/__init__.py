from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Database configuration
    database_url = os.getenv(
        'DATABASE_URL',
        'postgresql://dev_user:dev_password@localhost:5432/userservice_db'
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app