from . import auth_bp
from flask import request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models import Evaluator, Admin

@auth_bp.route('/token', methods=['POST'])
def login():
    data = request.get_json()
    siape_or_cpf = data.get('siape_or_cpf')
    password = data.get('password')
    evaluator = Evaluator.query.filter_by(siape_or_cpf=siape_or_cpf).first()
    if not evaluator:
        return jsonify({'msg': 'Credenciais inválidas.'}), 401
    if evaluator.password_hash:
        if not check_password_hash(evaluator.password_hash, password):
            return jsonify({'msg': 'Credenciais inválidas.'}), 401
    else:
        if evaluator.birthdate != password:
            return jsonify({'msg': 'Credenciais inválidas.'}), 401
    access_token = create_access_token(identity=str(evaluator.id))
    return jsonify({'access_token': access_token, 'role': 'evaluator'}), 200

@auth_bp.route('/admin/token', methods=['POST'])
def login_admin():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')
    admin = Admin.query.filter_by(login=login).first()
    if not admin or not check_password_hash(admin.password_hash, password):
        return jsonify({'msg': 'Credenciais inválidas.'}), 401
    access_token = create_access_token(identity=f'admin:{admin.id}')
    return jsonify({'access_token': access_token, 'role': 'admin'}), 200 