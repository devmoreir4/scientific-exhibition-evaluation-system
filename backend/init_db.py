from app import create_app
from app.extensions import db
from app.models import Evaluator, Work, Admin
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    admin_login = os.getenv('ADMIN_LOGIN', 'admin')
    admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
    if not Admin.query.filter_by(login=admin_login).first():
        admin = Admin(
            name='Administrador',
            login=admin_login,
            password_hash=generate_password_hash(admin_password)
        )
        db.session.add(admin)

    db.session.commit()
    print('Tables created successfully!')
