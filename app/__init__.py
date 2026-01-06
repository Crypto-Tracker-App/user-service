from flask import Flask
from os import getenv
from flasgger import Swagger
import logging

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
                'bearerFormat': 'JWT',
                'in': 'header',
                'description': 'JWT Bearer token authentication',
            }
        }
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Register blueprints
    from .api import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app