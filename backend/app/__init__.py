from flask import Flask
from flask_cors import CORS
from .extensions import db, jwt
import os
from .config import DevelopmentConfig, ProductionConfig, TestingConfig


def create_app():
    app = Flask(__name__)

    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }

    config_class = config_map.get(os.environ.get('FLASK_ENV', 'development'))
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

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
