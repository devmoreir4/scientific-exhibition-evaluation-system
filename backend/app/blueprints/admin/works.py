from . import admin_bp
from flask import jsonify, request
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from app.models import Work, Evaluator
from app.extensions import db
from app.services.csv_importer_service import import_works_from_csv
from app.services.evaluation_service import calculate_evaluation_progress, generate_works_podium
import io
from .misc import admin_required


@admin_bp.route('/works', methods=['GET'])
@jwt_required()
@admin_required
@swag_from({
    'tags': ['Admin - Trabalhos'],
    'summary': 'Listar trabalhos',
    'description': 'Lista todos os trabalhos com paginação',
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
            'description': 'Itens por página',
            'default': 20
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de trabalhos',
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
        403: {'description': 'Acesso negado'}
    }
})
def list_works():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    if per_page not in [10, 20, 30, 40, 50]:
        per_page = 10

    pagination = Work.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    works = pagination.items

    return jsonify({'works': [
        {'id': w.id, 'title': w.title, 'authors': w.authors, 'advisor': w.advisor,
            'type': w.type, 'area': w.area, 'subarea': w.subarea}
        for w in works
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


@admin_bp.route('/works/distributions', methods=['GET'])
@jwt_required()
@admin_required
@swag_from({
    'tags': ['Admin - Trabalhos'],
    'summary': 'Ver distribuições',
    'description': 'Lista como os trabalhos foram distribuídos entre os avaliadores',
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
            'description': 'Itens por página',
            'default': 20
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de distribuições de trabalhos',
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
                                'evaluators': {
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
                    }
                }
            }
        },
        403: {'description': 'Acesso negado'}
    }
})
def list_work_distributions():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    if per_page not in [10, 20, 30, 40, 50]:
        per_page = 10

    pagination = Work.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    works = pagination.items
    distributions = []

    for work in works:
        evaluators = []
        for evaluator in work.evaluators:
            evaluators.append({
                'id': evaluator.id,
                'name': evaluator.name,
                'siape_or_cpf': evaluator.siape_or_cpf,
                'area': evaluator.area,
                'subareas': evaluator.subareas,
                'workload': evaluator.workload
            })

        distributions.append({
            'work_id': work.id,
            'work_title': work.title,
            'work_authors': work.authors,
            'work_advisor': work.advisor,
            'work_type': work.type,
            'work_area': work.area,
            'work_subarea': work.subarea,
            'evaluators': evaluators,
            'evaluators_count': len(evaluators)
        })

    return jsonify({'distributions': distributions,
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


@admin_bp.route('/works', methods=['POST'])
@jwt_required()
@admin_required
@swag_from({
    'tags': ['Admin - Trabalhos'],
    'summary': 'Criar trabalho',
    'description': 'Cria um novo trabalho científico',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['title', 'authors', 'advisor', 'type', 'area', 'subarea'],
                'properties': {
                    'title': {'type': 'string', 'example': 'Desenvolvimento de Sistema IA'},
                    'authors': {'type': 'string', 'example': 'João Silva, Maria Santos'},
                    'advisor': {'type': 'string', 'example': 'Dr. Carlos Oliveira'},
                    'type': {'type': 'string', 'example': 'Pôster'},
                    'area': {'type': 'string', 'example': 'Computação'},
                    'subarea': {'type': 'string', 'example': 'Inteligência Artificial'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Trabalho criado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string', 'example': 'Trabalho criado com sucesso!'},
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
        400: {'description': 'Dados inválidos'},
        403: {'description': 'Acesso negado'}
    }
})
def create_work():
    data = request.get_json()

    required_fields = ['title', 'authors',
                       'advisor', 'type', 'area', 'subarea']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'msg': f'Campo {field} é obrigatório'}), 400

    work = Work(
        title=data['title'],
        authors=data['authors'],
        advisor=data['advisor'],
        type=data['type'],
        area=data['area'],
        subarea=data['subarea']
    )

    db.session.add(work)
    db.session.commit()

    return jsonify({
        'msg': 'Trabalho criado com sucesso!',
        'work': {
            'id': work.id,
            'title': work.title,
            'authors': work.authors,
            'advisor': work.advisor,
            'type': work.type,
            'area': work.area,
            'subarea': work.subarea
        }
    }), 201


@admin_bp.route('/works/import-csv', methods=['POST'])
@jwt_required()
@admin_required
@swag_from({
    'tags': ['Admin - Trabalhos'],
    'summary': 'Importar trabalhos via CSV',
    'description': 'Importa múltiplos trabalhos através de arquivo CSV',
    'security': [{'Bearer': []}],
    'consumes': ['multipart/form-data'],
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'Arquivo CSV com os trabalhos'
        }
    ],
    'responses': {
        200: {
            'description': 'Importação realizada com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string'},
                    'imported_count': {'type': 'integer'}
                }
            }
        },
        400: {
            'description': 'Erro na importação',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string'},
                    'errors': {'type': 'array', 'items': {'type': 'string'}},
                    'imported_count': {'type': 'integer'}
                }
            }
        },
        403: {'description': 'Acesso negado'}
    }
})
def import_works_csv():
    if 'file' not in request.files:
        return jsonify({'msg': 'Arquivo não enviado.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'msg': 'Nenhum arquivo selecionado.'}), 400

    filename = file.filename.lower()
    if not filename.endswith('.csv'):
        return jsonify({'msg': 'Arquivo deve ser CSV (.csv).'}), 400

    try:
        file_content = file.read()
        file_stream = io.StringIO(file_content.decode('utf-8'))
        result = import_works_from_csv(file_stream)
    except Exception as e:
        return jsonify({'msg': f'Erro ao processar arquivo CSV: {str(e)}'}), 500

    if result['success']:
        return jsonify({
            'msg': result['message'],
            'imported_count': result['imported_count']
        }), 200
    else:
        return jsonify({
            'msg': result['message'],
            'errors': result['errors'],
            'imported_count': result['imported_count']
        }), 400


@admin_bp.route('/works/<int:work_id>', methods=['DELETE'])
@jwt_required()
@admin_required
@swag_from({
    'tags': ['Admin - Trabalhos'],
    'summary': 'Remover trabalho',
    'description': 'Remove um trabalho do sistema',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'work_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do trabalho a ser removido'
        }
    ],
    'responses': {
        200: {
            'description': 'Trabalho removido com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string', 'example': 'Trabalho removido com sucesso!'}
                }
            }
        },
        404: {'description': 'Trabalho não encontrado'},
        403: {'description': 'Acesso negado'}
    }
})
def delete_work(work_id):
    work = Work.query.get(work_id)
    if not work:
        return jsonify({'msg': 'Trabalho não encontrado.'}), 404
    db.session.delete(work)
    db.session.commit()
    return jsonify({'msg': 'Trabalho removido com sucesso!'}), 200


@admin_bp.route('/works/<int:work_id>', methods=['PUT'])
@jwt_required()
@admin_required
@swag_from({
    'tags': ['Admin - Trabalhos'],
    'summary': 'Atualizar trabalho',
    'description': 'Atualiza dados de um trabalho existente',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'work_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do trabalho a ser atualizado'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string', 'example': 'Novo Título do Trabalho'},
                    'authors': {'type': 'string', 'example': 'Novos Autores'},
                    'advisor': {'type': 'string', 'example': 'Novo Orientador'},
                    'type': {'type': 'string', 'example': 'Pôster'},
                    'area': {'type': 'string', 'example': 'Computação'},
                    'subarea': {'type': 'string', 'example': 'Inteligência Artificial'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Trabalho atualizado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string', 'example': 'Trabalho atualizado com sucesso!'}
                }
            }
        },
        404: {'description': 'Trabalho não encontrado'},
        403: {'description': 'Acesso negado'}
    }
})
def update_work(work_id):
    work = Work.query.get(work_id)
    if not work:
        return jsonify({'msg': 'Trabalho não encontrado.'}), 404
    data = request.get_json()
    work.title = data.get('title', work.title)
    work.authors = data.get('authors', work.authors)
    work.advisor = data.get('advisor', work.advisor)
    work.type = data.get('type', work.type)
    work.area = data.get('area', work.area)
    work.subarea = data.get('subarea', work.subarea)
    db.session.commit()
    return jsonify({'msg': 'Trabalho atualizado com sucesso!'}), 200


@admin_bp.route('/works/evaluation-progress', methods=['GET'])
@jwt_required()
@admin_required
@swag_from({
    'tags': ['Admin - Monitoramento'],
    'summary': 'Progresso das avaliações',
    'description': 'Mostra o progresso atual das avaliações de todos os trabalhos',
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
            'description': 'Itens por página',
            'default': 20
        }
    ],
    'responses': {
        200: {
            'description': 'Dados do progresso das avaliações',
            'schema': {
                'type': 'object',
                'properties': {
                    'works_progress': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'work_id': {'type': 'integer'},
                                'work_title': {'type': 'string'},
                                'total_evaluators': {'type': 'integer'},
                                'completed_evaluations': {'type': 'integer'},
                                'progress_percentage': {'type': 'number'}
                            }
                        }
                    },
                    'summary': {
                        'type': 'object',
                        'properties': {
                            'total_works': {'type': 'integer'},
                            'completed_works': {'type': 'integer'},
                            'overall_progress': {'type': 'number'}
                        }
                    }
                }
            }
        },
        403: {'description': 'Acesso negado'}
    }
})
def get_evaluation_progress():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    if per_page not in [10, 20, 30, 40, 50]:
        per_page = 10

    progress_data = calculate_evaluation_progress(page=page, per_page=per_page)
    return jsonify(progress_data), 200


@admin_bp.route('/works/podium', methods=['GET'])
@jwt_required()
@admin_required
@swag_from({
    'tags': ['Admin - Monitoramento'],
    'summary': 'Gerar pódio',
    'description': 'Gera o pódio/ranking dos trabalhos baseado nas avaliações',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Dados do pódio dos trabalhos',
            'schema': {
                'type': 'object',
                'properties': {
                    'podium_data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'position': {'type': 'integer'},
                                'work_id': {'type': 'integer'},
                                'work_title': {'type': 'string'},
                                'work_authors': {'type': 'string'},
                                'average_score': {'type': 'number'},
                                'total_evaluations': {'type': 'integer'},
                                'area': {'type': 'string'},
                                'subarea': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        },
        403: {'description': 'Acesso negado'}
    }
})
def get_works_podium():
    podium_data = generate_works_podium()
    return jsonify({'podium_data': podium_data}), 200


@admin_bp.route('/works/evaluator/<int:evaluator_id>', methods=['GET'])
@jwt_required()
@admin_required
@swag_from({
    'tags': ['Admin - Trabalhos'],
    'summary': 'Trabalhos de um avaliador',
    'description': 'Lista todos os trabalhos atribuídos a um avaliador específico',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'evaluator_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do avaliador'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de trabalhos do avaliador',
            'schema': {
                'type': 'object',
                'properties': {
                    'evaluator': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'name': {'type': 'string'},
                            'workload': {'type': 'integer'}
                        }
                    },
                    'works': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'title': {'type': 'string'},
                                'authors': {'type': 'string'},
                                'area': {'type': 'string'},
                                'subarea': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        },
        404: {'description': 'Avaliador não encontrado'},
        403: {'description': 'Acesso negado'}
    }
})
def get_works_by_evaluator(evaluator_id):
    evaluator = Evaluator.query.get(evaluator_id)
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
