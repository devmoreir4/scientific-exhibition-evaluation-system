from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from .extensions import db, jwt
import os
from .config import DevelopmentConfig, ProductionConfig, LocalDevelopmentConfig


def create_app():
    app = Flask(__name__)

    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'local': LocalDevelopmentConfig
    }

    config_class = config_map.get(os.environ.get('FLASK_ENV', 'development'))
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    # Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'api_docs',
                "route": '/api/v1/docs.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/v1/docs/"
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Sistema de Avaliação para Mostra Científica",
            "description": "API REST completa para gerenciamento, distribuição e avaliação de trabalhos científicos",
            "version": "1.0.0"
        },
        "host": "localhost:5000",
        "basePath": "/api/v1",
        "schemes": ["http"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Token JWT no formato: Bearer {token}"
            }
        },
        "security": [{"Bearer": []}],
        "consumes": ["application/json"],
        "produces": ["application/json"]
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:4173", "http://127.0.0.1:4173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # blueprints
    from .blueprints.auth import auth_bp
    from .blueprints.admin import admin_bp
    from .blueprints.evaluator import evaluator_bp

    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
    app.register_blueprint(evaluator_bp, url_prefix='/api/v1/evaluator')

    return app
