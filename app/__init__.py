from flask import Flask
from os import getenv
from flasgger import Swagger

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
    
    # Configure Swagger/OpenAPI
    swagger_config = {
        'specs': [
            {
                'endpoint': 'apispec',
                'route': '/apispec.json'
            }
        ],
        'specs_route': '/apidocs/',
        'static_url_path': '/flasgger_static',
        'swagger_ui': True,
        'headers': []
    }
    
    swagger_template = {
        'swagger': '2.0',
        'info': {
            'title': 'User Service API',
            'description': 'Authentication and user management API',
            'version': '1.0.0'
        },
        'securityDefinitions': {
            'SessionAuth': {
                'type': 'apiKey',
                'name': 'session_id',
                'in': 'cookie',
                'description': 'Session-based authentication'
            }
        }
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Register blueprints
    from .api import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app