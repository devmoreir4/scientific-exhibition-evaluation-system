from . import evaluator_bp
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Evaluation, Work, Evaluator
from app.extensions import db
from app.services.evaluation_service import (
    validate_evaluation_data, create_evaluation,
    get_evaluator_evaluations, get_work_evaluations
)

@evaluator_bp.route('/evaluations', methods=['POST'])
@jwt_required()
def submit_evaluation():
    evaluator_id = int(get_jwt_identity())
    data = request.get_json()
    work_id = data.get('work_id')

    is_valid, result = validate_evaluation_data(data, evaluator_id, work_id)

    if not is_valid:
        error_msg = '; '.join(result)
        return jsonify({'msg': error_msg}), 400

    criteria = result

    create_evaluation(evaluator_id, work_id, criteria)

    return jsonify({'msg': 'Avaliação registrada com sucesso!'}), 201

@evaluator_bp.route('/evaluations/mine', methods=['GET'])
@jwt_required()
def list_my_evaluations():
    evaluator_id = int(get_jwt_identity())
    evaluations = get_evaluator_evaluations(evaluator_id)
    return jsonify({'evaluations': evaluations}), 200

@evaluator_bp.route('/evaluations/work/<int:work_id>', methods=['GET'])
@jwt_required()
def list_evaluations_for_work(work_id):
    evaluations = get_work_evaluations(work_id)
    return jsonify({'evaluations': evaluations}), 200
