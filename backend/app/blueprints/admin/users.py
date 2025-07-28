from . import admin_bp
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Evaluator
from app.extensions import db

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    users = Evaluator.query.all()
    return jsonify({'users': [
        {'id': u.id, 'name': u.name, 'siape_or_cpf': u.siape_or_cpf, 'birthdate': u.birthdate, 'area': u.area, 'subareas': u.subareas, 'carga': u.carga}
        for u in users
    ]}), 200

@admin_bp.route('/users/simple', methods=['GET'])
@jwt_required()
def list_users_simple():
    users = Evaluator.query.all()
    return jsonify({'users': [
        {'id': u.id, 'name': u.name}
        for u in users
    ]}), 200

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = Evaluator.query.get(user_id)
    if not user:
        return jsonify({'msg': 'Usuário não encontrado.'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': 'Usuário removido com sucesso!'}), 200

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = Evaluator.query.get(user_id)
    if not user:
        return jsonify({'msg': 'Usuário não encontrado.'}), 404
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.siape_or_cpf = data.get('siape_or_cpf', user.siape_or_cpf)
    user.birthdate = data.get('birthdate', user.birthdate)
    user.area = data.get('area', user.area)
    user.subareas = data.get('subareas', user.subareas)
    db.session.commit()
    return jsonify({'msg': 'Usuário atualizado com sucesso!'}), 200 