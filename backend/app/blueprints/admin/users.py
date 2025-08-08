from . import admin_bp
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Evaluator
from app.extensions import db
from app.services.auth_service import (
    validate_siape_or_cpf, validate_birthdate, sanitize_evaluator_data,
    validate_evaluator_registration, create_evaluator
)
from .misc import admin_required

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def list_users():
    users = Evaluator.query.all()
    return jsonify({'users': [
        {'id': u.id, 'name': u.name, 'siape_or_cpf': u.siape_or_cpf, 'birthdate': u.birthdate, 'area': u.area, 'subareas': u.subareas, 'workload': u.workload}
        for u in users
    ]}), 200

@admin_bp.route('/users/simple', methods=['GET'])
@jwt_required()
@admin_required
def list_users_simple():
    users = Evaluator.query.all()
    return jsonify({'users': [
        {'id': u.id, 'name': u.name}
        for u in users
    ]}), 200

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    user = Evaluator.query.get(user_id)
    if not user:
        return jsonify({'msg': 'Usuário não encontrado.'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': 'Usuário removido com sucesso!'}), 200

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    user = Evaluator.query.get(user_id)
    if not user:
        return jsonify({'msg': 'Usuário não encontrado.'}), 404

    data = request.get_json()

    # Sanitizar dados de entrada
    clean_data = sanitize_evaluator_data(data)

    # Validar SIAPE/CPF se foi alterado
    new_siape_or_cpf = clean_data.get('siape_or_cpf')
    if new_siape_or_cpf and new_siape_or_cpf != user.siape_or_cpf:
        is_valid, msg = validate_siape_or_cpf(new_siape_or_cpf)
        if not is_valid:
            return jsonify({'msg': msg}), 400

        # Verificar se já existe outro usuário com este SIAPE/CPF
        existing = Evaluator.query.filter_by(siape_or_cpf=new_siape_or_cpf).first()
        if existing and existing.id != user_id:
            return jsonify({'msg': 'SIAPE ou CPF já cadastrado por outro usuário'}), 409

    # Validar data de nascimento se foi alterada
    new_birthdate = clean_data.get('birthdate')
    if new_birthdate and new_birthdate != user.birthdate:
        is_valid, msg = validate_birthdate(new_birthdate)
        if not is_valid:
            return jsonify({'msg': msg}), 400

    # Atualizar campos
    user.name = clean_data.get('name', user.name)
    user.siape_or_cpf = new_siape_or_cpf or user.siape_or_cpf
    user.birthdate = new_birthdate or user.birthdate
    user.area = clean_data.get('area', user.area)
    user.subareas = clean_data.get('subareas', user.subareas)
    user.workload = data.get('workload', user.workload)  # workload não precisa sanitizar

    db.session.commit()
    return jsonify({'msg': 'Usuário atualizado com sucesso!'}), 200

@admin_bp.route('/users', methods=['POST'])
@jwt_required()
@admin_required
def create_user():
    data = request.get_json()

    # Sanitizar dados de entrada
    clean_data = sanitize_evaluator_data(data)

    # Validar dados de registro usando o service
    is_valid, result = validate_evaluator_registration(clean_data)

    if not is_valid:
        error_msg = '; '.join(result)
        status_code = 409 if 'já cadastrado' in error_msg else 400
        return jsonify({'msg': error_msg}), status_code

    # Criar novo usuário usando o service
    evaluator = create_evaluator(result)

    return jsonify({
        'msg': 'Usuário criado com sucesso!',
        'user': {
            'id': evaluator.id,
            'name': evaluator.name,
            'siape_or_cpf': evaluator.siape_or_cpf,
            'area': evaluator.area,
            'subareas': evaluator.subareas
        }
    }), 201
