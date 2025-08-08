from . import auth_bp
from flask import request, jsonify
from app.services.auth_service import (
    validate_evaluator_registration, create_evaluator, sanitize_evaluator_data
)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Sanitize input data
    clean_data = sanitize_evaluator_data(data)

    # Validate registration data
    is_valid, result = validate_evaluator_registration(clean_data)

    if not is_valid:
        error_msg = '; '.join(result)
        status_code = 409 if 'já cadastrado' in error_msg else 400
        return jsonify({'msg': error_msg}), status_code

    # Create new evaluator
    evaluator = create_evaluator(result)

    return jsonify({'msg': 'Avaliador cadastrado com sucesso!'}), 201
