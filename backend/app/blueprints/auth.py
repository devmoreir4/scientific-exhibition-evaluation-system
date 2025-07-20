from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models import Evaluator

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')  # data de nascimento
    type_ = data.get('type')  # 'pedagogico' ou 'tecnico'

    if not all([name, email, password, type_]):
        return jsonify({'msg': 'Dados obrigatórios faltando.'}), 400

    if Evaluator.query.filter_by(email=email).first():
        return jsonify({'msg': 'Email já cadastrado.'}), 409

    password_hash = generate_password_hash(password)
    evaluator = Evaluator(name=name, email=email, password_hash=password_hash, type=type_)
    db.session.add(evaluator)
    db.session.commit()
    return jsonify({'msg': 'Avaliador cadastrado com sucesso!'}), 201

@auth_bp.route('/token', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    evaluator = Evaluator.query.filter_by(email=email).first()
    if not evaluator or not check_password_hash(evaluator.password_hash, password):
        return jsonify({'msg': 'Credenciais inválidas.'}), 401

    access_token = create_access_token(identity=str(evaluator.id))
    return jsonify({'access_token': access_token}), 200 