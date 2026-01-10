from flask import Flask
from os import getenv
from flasgger import Swagger
import logging

from .config import DevelopmentConfig, ProductionConfig, TestingConfig
from .extensions import db, bcrypt


def create_app():
    app = Flask(__name__)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Load configuration based on environment
    env = getenv('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object(ProductionConfig)
    elif env == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    
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
            'BearerAuth': {
                'type': 'apiKey',
                'name': 'Authorization',
                'scheme': 'bearer',
                'bearerFormat': 'bearer',
                'in': 'header',
                'description': 'Type in the *\'Value\'* input box below: **\'Bearer &lt;JWT&gt;\'**, where JWT is the token',
            }
        },
        'tags': [
            {
                'name': 'Health',
                'description': 'Health and readiness endpoints'
            }
        ]
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Register blueprints
    from .api import auth_blueprint
    from .api.health import health_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_blueprint, url_prefix='/api')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app