import time
import psycopg2
import os
from app import create_app
from app.extensions import db
from app.models import Admin
from werkzeug.security import generate_password_hash


def wait_for_postgres():
    max_retries = 30
    retry_interval = 2

    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=os.environ.get('DB_HOST', 'postgres'),
                port=int(os.environ.get('DB_PORT', 5432)),
                database=os.environ.get('DB_NAME', 'evaluation_system'),
                user=os.environ.get('DB_USER', 'postgres'),
                password=os.environ.get('DB_PASSWORD', 'postgres123')
            )
            conn.close()
            print(f"PostgreSQL is ready! (attempt {i+1})")
            return True
        except psycopg2.OperationalError as e:
            print(f"Waiting for PostgreSQL... (attempt {i+1}/{max_retries})")
            if i < max_retries - 1:
                time.sleep(retry_interval)
            else:
                print("Failed to connect to PostgreSQL after all attempts. Error:", e)
                return False

    return False


app = create_app()


if __name__ == "__main__":
    print("Waiting for PostgreSQL to be ready...")
    if wait_for_postgres():
        with app.app_context():
            print("Creating all tables via SQLAlchemy...")
            db.create_all()

            print("Checking default admin...")

            admin_login = os.environ.get('ADMIN_LOGIN', 'admin')
            admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')

            admin = Admin.query.filter_by(login=admin_login).first()
            if not admin:
                admin = Admin(
                    login=admin_login,
                    name='Administrator',
                    password_hash=generate_password_hash(admin_password)
                )
                db.session.add(admin)
                db.session.commit()
                print(f'Default admin created: login={admin_login}, password={admin_password}')
            else:
                print(f'Admin already exists in system (login: {admin_login})')

            print('Database initialized successfully!')
    else:
        print("Database initialization failed.")
        exit(1)
