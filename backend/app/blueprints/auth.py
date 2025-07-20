from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models import Evaluator, Admin
from werkzeug.security import check_password_hash
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Cadastro de avaliador
    ---
    tags:
      - Autenticação
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - name
              - siape_or_cpf
              - birthdate
              - area
            properties:
              name:
                type: string
              siape_or_cpf:
                type: string
                description: SIAPE (servidor) ou CPF (externo)
              birthdate:
                type: string
                description: Data de nascimento (apenas números, formato DDMMAAAA)
              area:
                type: string
                description: Área de atuação
              subareas:
                type: string
                description: Subáreas de interesse (separadas por vírgula)
    responses:
      201:
        description: Avaliador cadastrado com sucesso
      400:
        description: Dados obrigatórios faltando ou formato inválido
      409:
        description: SIAPE ou CPF já cadastrado
    """
    data = request.get_json()
    name = data.get('name')
    siape_or_cpf = data.get('siape_or_cpf')
    birthdate = data.get('birthdate')
    area = data.get('area')
    subareas = data.get('subareas', '')

    if not all([name, siape_or_cpf, birthdate, area]):
        return jsonify({'msg': 'Dados obrigatórios faltando.'}), 400
    if not re.fullmatch(r'\d{8}', birthdate):
        return jsonify({'msg': 'A data de nascimento deve conter 8 dígitos (DDMMAAAA).'}), 400

    if Evaluator.query.filter_by(siape_or_cpf=siape_or_cpf).first():
        return jsonify({'msg': 'SIAPE ou CPF já cadastrado.'}), 409

    evaluator = Evaluator(name=name, siape_or_cpf=siape_or_cpf, birthdate=birthdate, area=area, subareas=subareas)
    db.session.add(evaluator)
    db.session.commit()
    return jsonify({'msg': 'Avaliador cadastrado com sucesso!'}), 201

@auth_bp.route('/token', methods=['POST'])
def login():
    """
    Login de avaliador
    ---
    tags:
      - Autenticação
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - siape_or_cpf
              - birthdate
            properties:
              siape_or_cpf:
                type: string
                description: SIAPE (servidor) ou CPF (externo)
              birthdate:
                type: string
                description: Data de nascimento (apenas números, formato DDMMAAAA)
    responses:
      200:
        description: Token JWT gerado com sucesso
      401:
        description: Credenciais inválidas
    """
    data = request.get_json()
    siape_or_cpf = data.get('siape_or_cpf')
    birthdate = data.get('birthdate')

    evaluator = Evaluator.query.filter_by(siape_or_cpf=siape_or_cpf).first()
    if not evaluator or evaluator.birthdate != birthdate:
        return jsonify({'msg': 'Credenciais inválidas.'}), 401

    access_token = create_access_token(identity=str(evaluator.id))
    return jsonify({'access_token': access_token, 'role': 'evaluator'}), 200

# --- Login de admin ---
@auth_bp.route('/admin/token', methods=['POST'])
def login_admin():
    """
    Login de administrador
    ---
    tags:
      - Autenticação
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - login
              - password
            properties:
              login:
                type: string
              password:
                type: string
    responses:
      200:
        description: Token JWT gerado com sucesso
      401:
        description: Credenciais inválidas
    """
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')

    admin = Admin.query.filter_by(login=login).first()
    if not admin or not check_password_hash(admin.password_hash, password):
        return jsonify({'msg': 'Credenciais inválidas.'}), 401

    access_token = create_access_token(identity=f'admin:{admin.id}')
    return jsonify({'access_token': access_token, 'role': 'admin'}), 200 