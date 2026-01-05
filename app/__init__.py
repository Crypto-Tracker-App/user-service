from flask import Flask
from os import getenv
import logging

from .config import ProductionConfig
from .extensions import db, session_manager


def create_app():
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    app.config.from_object(ProductionConfig)

    
    # Initialize extensions
    db.init_app(app)
    session_manager.init_app(app)
    
    # Register blueprints
    from .api import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app