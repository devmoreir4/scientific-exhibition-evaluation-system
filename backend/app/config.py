import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ALGORITHM = os.environ.get('ALGORITHM', 'HS256')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 30))
    )
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads') 