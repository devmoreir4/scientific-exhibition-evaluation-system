import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    DB_HOST = os.environ.get('DB_HOST', 'postgres')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'evaluation_system')
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres123')

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ALGORITHM = os.environ.get('ALGORITHM', 'HS256')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 60))
    )
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'
