from . import evaluator_bp
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.services.evaluation_service import (
    validate_evaluation_data, create_evaluation,
    get_evaluator_evaluations, get_work_evaluations
)


@evaluator_bp.route('/evaluations', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Avaliador'],
    'summary': 'Enviar avaliação',
    'description': 'Submete avaliação de um trabalho',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['work_id', 'criterion1', 'criterion2', 'criterion3', 'criterion4', 'criterion5'],
                'properties': {
                    'work_id': {'type': 'integer', 'example': 1},
                    'criterion1': {'type': 'number', 'minimum': 1, 'maximum': 5, 'example': 4},
                    'criterion2': {'type': 'number', 'minimum': 1, 'maximum': 5, 'example': 5},
                    'criterion3': {'type': 'number', 'minimum': 1, 'maximum': 5, 'example': 3},
                    'criterion4': {'type': 'number', 'minimum': 1, 'maximum': 5, 'example': 4},
                    'criterion5': {'type': 'number', 'minimum': 1, 'maximum': 5, 'example': 5}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Avaliação registrada com sucesso'},
        400: {'description': 'Dados inválidos'},
        404: {'description': 'Trabalho não encontrado ou não atribuído'}
    }
})
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
@swag_from({
    'tags': ['Avaliador'],
    'summary': 'Minhas avaliações',
    'description': 'Lista todas as avaliações realizadas pelo avaliador logado',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Lista de avaliações do avaliador',
            'schema': {
                'type': 'object',
                'properties': {
                    'evaluations': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'work_id': {'type': 'integer'},
                                'work_title': {'type': 'string'},
                                'criterion1': {'type': 'number'},
                                'criterion2': {'type': 'number'},
                                'criterion3': {'type': 'number'},
                                'criterion4': {'type': 'number'},
                                'criterion5': {'type': 'number'},
                                'method': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        },
        401: {'description': 'Token inválido'}
    }
})
def list_my_evaluations():
    evaluator_id = int(get_jwt_identity())
    evaluations = get_evaluator_evaluations(evaluator_id)
    return jsonify({'evaluations': evaluations}), 200


@evaluator_bp.route('/evaluations/work/<int:work_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Avaliador'],
    'summary': 'Avaliações de um trabalho',
    'description': 'Lista avaliações de um trabalho específico',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'work_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do trabalho'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de avaliações do trabalho',
            'schema': {
                'type': 'object',
                'properties': {
                    'evaluations': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'evaluator_name': {'type': 'string'},
                                'criterion1': {'type': 'number'},
                                'criterion2': {'type': 'number'},
                                'criterion3': {'type': 'number'},
                                'criterion4': {'type': 'number'},
                                'criterion5': {'type': 'number'},
                                'method': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        },
        401: {'description': 'Token inválido'}
    }
})
def list_evaluations_for_work(work_id):
    evaluations = get_work_evaluations(work_id)
    return jsonify({'evaluations': evaluations}), 200
