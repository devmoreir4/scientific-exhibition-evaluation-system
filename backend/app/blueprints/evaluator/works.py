from . import evaluator_bp
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.models import Evaluator

@evaluator_bp.route('/works/assigned', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Avaliador'],
    'summary': 'Trabalhos atribuídos',
    'description': 'Lista trabalhos atribuídos ao avaliador logado',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Lista de trabalhos atribuídos',
            'schema': {
                'type': 'object',
                'properties': {
                    'works': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'title': {'type': 'string'},
                                'authors': {'type': 'string'},
                                'advisor': {'type': 'string'},
                                'type': {'type': 'string'},
                                'area': {'type': 'string'},
                                'subarea': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        },
        404: {'description': 'Avaliador não encontrado'}
    }
})
def get_assigned_works():
    evaluator = Evaluator.query.get(int(get_jwt_identity()))
    if not evaluator:
        return jsonify({'msg': 'Avaliador não encontrado.'}), 404
    works = [
        {
            'id': w.id,
            'title': w.title,
            'authors': w.authors,
            'advisor': w.advisor,
            'type': w.type,
            'area': w.area,
            'subarea': w.subarea
        }
        for w in evaluator.works
    ]
    return jsonify({'works': works}), 200

@evaluator_bp.route('/works/<int:work_id>', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Avaliador'],
    'summary': 'Detalhes do trabalho',
    'description': 'Obtém detalhes de um trabalho específico atribuído ao avaliador',
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
            'description': 'Detalhes do trabalho',
            'schema': {
                'type': 'object',
                'properties': {
                    'work': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'title': {'type': 'string'},
                            'authors': {'type': 'string'},
                            'advisor': {'type': 'string'},
                            'type': {'type': 'string'},
                            'area': {'type': 'string'},
                            'subarea': {'type': 'string'}
                        }
                    }
                }
            }
        },
        404: {'description': 'Trabalho não encontrado ou não atribuído'},
        401: {'description': 'Token inválido'}
    }
})
def get_work(work_id):
    evaluator = Evaluator.query.get(int(get_jwt_identity()))
    if not evaluator:
        return jsonify({'msg': 'Avaliador não encontrado.'}), 404
    work = next((w for w in evaluator.works if w.id == work_id), None)
    if not work:
        return jsonify({'msg': 'Trabalho não encontrado ou não atribuído a você.'}), 404
    return jsonify({'work': {
        'id': work.id,
        'title': work.title,
        'authors': work.authors,
        'advisor': work.advisor,
        'type': work.type,
        'area': work.area,
        'subarea': work.subarea
    }}), 200
