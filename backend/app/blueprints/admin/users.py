from . import admin_bp
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flasgger import swag_from
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
@swag_from({
    'tags': ['Admin - Usuários'],
    'summary': 'Listar avaliadores',
    'description': 'Lista todos os avaliadores com paginação',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'description': 'Número da página',
            'default': 1
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'description': 'Itens por página (10, 20, 30, 40, 50)',
            'default': 20
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de avaliadores',
            'schema': {
                'type': 'object',
                'properties': {
                    'users': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'name': {'type': 'string'},
                                'siape_or_cpf': {'type': 'string'},
                                'birthdate': {'type': 'string'},
                                'area': {'type': 'string'},
                                'subareas': {'type': 'string'},
                                'workload': {'type': 'integer'}
                            }
                        }
                    }
                }
            }
        },
        403: {'description': 'Acesso negado'}
    }
})
def list_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    if per_page not in [10, 20, 30, 40, 50]:
        per_page = 10

    pagination = Evaluator.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    users = pagination.items

    return jsonify({'users': [
        {'id': u.id, 'name': u.name, 'siape_or_cpf': u.siape_or_cpf, 'birthdate': u.birthdate,
            'area': u.area, 'subareas': u.subareas, 'workload': u.workload}
        for u in users
    ],
        'pagination': {
        'page': pagination.page,
        'per_page': pagination.per_page,
        'pages': pagination.pages,
        'total': pagination.total,
        'has_prev': pagination.has_prev,
        'has_next': pagination.has_next,
        'prev_num': pagination.prev_num,
        'next_num': pagination.next_num
    }}), 200


@admin_bp.route('/users/simple', methods=['GET'])
@jwt_required()
@admin_required
@swag_from({
    'tags': ['Admin - Usuários'],
    'summary': 'Listar avaliadores (simplificado)',
    'description': 'Lista simplificada de avaliadores (apenas ID e nome)',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Lista simplificada de avaliadores',
            'schema': {
                'type': 'object',
                'properties': {
                    'users': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'name': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        },
        403: {'description': 'Acesso negado'}
    }
})
def list_users_simple():
    users = Evaluator.query.all()
    return jsonify({'users': [
        {'id': u.id, 'name': u.name}
        for u in users
    ]}), 200


@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
@swag_from({
    'tags': ['Admin - Usuários'],
    'summary': 'Remover avaliador',
    'description': 'Remove um avaliador do sistema',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário a ser removido'
        }
    ],
    'responses': {
        200: {
            'description': 'Usuário removido com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string', 'example': 'Usuário removido com sucesso!'}
                }
            }
        },
        404: {'description': 'Usuário não encontrado'},
        403: {'description': 'Acesso negado'}
    }
})
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
@swag_from({
    'tags': ['Admin - Usuários'],
    'summary': 'Atualizar avaliador',
    'description': 'Atualiza dados de um avaliador existente',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário a ser atualizado'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'João Silva Santos'},
                    'siape_or_cpf': {'type': 'string', 'example': '11122233344'},
                    'birthdate': {'type': 'string', 'example': '15031990'},
                    'area': {'type': 'string', 'example': 'Computação'},
                    'subareas': {'type': 'string', 'example': 'Inteligência Artificial;Machine Learning'},
                    'workload': {'type': 'integer', 'example': 5}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Usuário atualizado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string', 'example': 'Usuário atualizado com sucesso!'}
                }
            }
        },
        400: {'description': 'Dados inválidos'},
        404: {'description': 'Usuário não encontrado'},
        409: {'description': 'SIAPE/CPF já cadastrado por outro usuário'},
        403: {'description': 'Acesso negado'}
    }
})
def update_user(user_id):
    user = Evaluator.query.get(user_id)
    if not user:
        return jsonify({'msg': 'Usuário não encontrado.'}), 404

    data = request.get_json()

    clean_data = sanitize_evaluator_data(data)

    new_siape_or_cpf = clean_data.get('siape_or_cpf')
    if new_siape_or_cpf and new_siape_or_cpf != user.siape_or_cpf:
        is_valid, msg = validate_siape_or_cpf(new_siape_or_cpf)
        if not is_valid:
            return jsonify({'msg': msg}), 400

        existing = Evaluator.query.filter_by(
            siape_or_cpf=new_siape_or_cpf).first()
        if existing and existing.id != user_id:
            return jsonify({'msg': 'SIAPE ou CPF já cadastrado por outro usuário'}), 409

    new_birthdate = clean_data.get('birthdate')
    if new_birthdate and new_birthdate != user.birthdate:
        is_valid, msg = validate_birthdate(new_birthdate)
        if not is_valid:
            return jsonify({'msg': msg}), 400

    user.name = clean_data.get('name', user.name)
    user.siape_or_cpf = new_siape_or_cpf or user.siape_or_cpf
    user.birthdate = new_birthdate or user.birthdate
    user.area = clean_data.get('area', user.area)
    user.subareas = clean_data.get('subareas', user.subareas)
    user.workload = data.get('workload', user.workload)

    db.session.commit()
    return jsonify({'msg': 'Usuário atualizado com sucesso!'}), 200


@admin_bp.route('/users', methods=['POST'])
@jwt_required()
@admin_required
@swag_from({
    'tags': ['Admin - Usuários'],
    'summary': 'Criar avaliador',
    'description': 'Cria um novo avaliador no sistema (versão admin)',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['name', 'siape_or_cpf', 'birthdate', 'area', 'subareas'],
                'properties': {
                    'name': {'type': 'string', 'example': 'Maria Santos Silva'},
                    'siape_or_cpf': {'type': 'string', 'example': '99988877766'},
                    'birthdate': {'type': 'string', 'example': '20051985'},
                    'area': {'type': 'string', 'example': 'Computação'},
                    'subareas': {'type': 'string', 'example': 'Inteligência Artificial;Machine Learning'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Usuário criado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string', 'example': 'Usuário criado com sucesso!'},
                    'user': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'name': {'type': 'string'},
                            'siape_or_cpf': {'type': 'string'},
                            'area': {'type': 'string'},
                            'subareas': {'type': 'string'}
                        }
                    }
                }
            }
        },
        400: {'description': 'Dados inválidos'},
        409: {'description': 'SIAPE/CPF já cadastrado'},
        403: {'description': 'Acesso negado'}
    }
})
def create_user():
    data = request.get_json()

    clean_data = sanitize_evaluator_data(data)

    is_valid, result = validate_evaluator_registration(clean_data)

    if not is_valid:
        error_msg = '; '.join(result)
        status_code = 409 if 'já cadastrado' in error_msg else 400
        return jsonify({'msg': error_msg}), status_code

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
