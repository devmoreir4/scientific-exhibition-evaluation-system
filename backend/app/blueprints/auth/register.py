from . import auth_bp
from flask import request, jsonify
from app.extensions import db
from app.models import Evaluator
import re

@auth_bp.route('/register', methods=['POST'])
def register():
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
