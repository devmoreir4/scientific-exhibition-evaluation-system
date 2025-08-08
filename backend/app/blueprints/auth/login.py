from . import auth_bp
from flask import request, jsonify
from app.services.auth_service import (
    authenticate_evaluator, authenticate_admin,
    generate_access_token, validate_login_credentials
)

@auth_bp.route('/token', methods=['POST'])
def login():
    data = request.get_json()

    # Validate login credentials
    is_valid, errors = validate_login_credentials(data, 'evaluator')
    if not is_valid:
        return jsonify({'msg': '; '.join(errors)}), 400

    # Authenticate evaluator
    siape_or_cpf = data.get('siape_or_cpf')
    password = data.get('password')

    evaluator, error_msg = authenticate_evaluator(siape_or_cpf, password)

    if not evaluator:
        return jsonify({'msg': error_msg}), 401

    # Generate access token
    access_token = generate_access_token(evaluator, 'evaluator')

    return jsonify({'access_token': access_token, 'role': 'evaluator'}), 200

@auth_bp.route('/admin/token', methods=['POST'])
def login_admin():
    data = request.get_json()

    # Validate login credentials
    is_valid, errors = validate_login_credentials(data, 'admin')
    if not is_valid:
        return jsonify({'msg': '; '.join(errors)}), 400

    # Authenticate admin
    login = data.get('login')
    password = data.get('password')

    admin, error_msg = authenticate_admin(login, password)

    if not admin:
        return jsonify({'msg': error_msg}), 401

    # Generate access token
    access_token = generate_access_token(admin, 'admin')

    return jsonify({'access_token': access_token, 'role': 'admin'}), 200
