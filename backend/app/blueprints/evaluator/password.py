from . import evaluator_bp
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import Evaluator
from app.extensions import db

@evaluator_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    evaluator_id = int(get_jwt_identity())
    evaluator = Evaluator.query.get(evaluator_id)
    if not evaluator:
        return jsonify({'msg': 'Avaliador não encontrado.'}), 404
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    if not current_password or not new_password:
        return jsonify({'msg': 'Senha atual e nova senha são obrigatórias.'}), 400
    if len(new_password) < 6:
        return jsonify({'msg': 'A nova senha deve ter pelo menos 6 caracteres.'}), 400
    current_password_valid = False
    if evaluator.password_hash:
        current_password_valid = check_password_hash(evaluator.password_hash, current_password)
    else:
        current_password_valid = (evaluator.birthdate == current_password)
    if not current_password_valid:
        return jsonify({'msg': 'Senha atual incorreta.'}), 401
    evaluator.password_hash = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({'msg': 'Senha alterada com sucesso!'}), 200
