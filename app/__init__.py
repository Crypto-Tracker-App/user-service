from flask import Flask
from os import getenv

from .config import DevelopmentConfig, ProductionConfig
from .extensions import db, session_manager


def create_app():
    app = Flask(__name__)
    
    # Load configuration based on environment
    env = getenv('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    
    # Initialize extensions
    db.init_app(app)
    session_manager.init_app(app)
    
    # Register blueprints
    from .api import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    
    @app.route('/health')
    def health():
        return {'status': 'ok'}, 200
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app