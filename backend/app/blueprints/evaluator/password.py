from . import evaluator_bp
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import (
    get_evaluator_by_id, validate_password_change,
    change_evaluator_password, is_password_strong
)

@evaluator_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    evaluator_id = int(get_jwt_identity())

    evaluator = get_evaluator_by_id(evaluator_id)
    if not evaluator:
        return jsonify({'msg': 'Avaliador não encontrado.'}), 404

    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    is_strong, strength_msg = is_password_strong(new_password)
    if not is_strong:
        return jsonify({'msg': strength_msg}), 400

    is_valid, errors = validate_password_change(evaluator, current_password, new_password)

    if not is_valid:
        error_msg = '; '.join(errors)
        status_code = 401 if 'incorreta' in error_msg else 400
        return jsonify({'msg': error_msg}), status_code

    change_evaluator_password(evaluator, new_password)

    return jsonify({'msg': 'Senha alterada com sucesso!'}), 200
