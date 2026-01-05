from flask import Flask
from os import getenv
import logging
from flask_cors import CORS

from .config import ProductionConfig
from .extensions import db, bcrypt


def create_app():
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    app.config.from_object(ProductionConfig)

    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Enable CORS for all routes
    CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})
    
    # Register blueprints
    from .api import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app