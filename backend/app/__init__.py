from flask import Flask
from .extensions import db, jwt
from .config import Config
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    Swagger(app)

    # Importar e registrar blueprints (placeholders)
    from .blueprints.auth import auth_bp
    from .blueprints.admin import admin_bp
    from .blueprints.evaluator import evaluator_bp

    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')
    app.register_blueprint(evaluator_bp, url_prefix='/api/v1/evaluator')

    return app 