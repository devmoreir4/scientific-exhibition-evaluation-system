from . import auth_bp
from flask import request, jsonify
from flasgger import swag_from
from app.services.auth_service import (
    validate_evaluator_registration, create_evaluator, sanitize_evaluator_data
)

@auth_bp.route('/register', methods=['POST'])
@swag_from({
    'tags': ['Autenticação'],
    'summary': 'Registro de avaliador',
    'description': 'Cadastra um novo avaliador no sistema',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['name', 'siape_or_cpf', 'birthdate', 'area', 'subareas'],
                'properties': {
                    'name': {
                        'type': 'string',
                        'description': 'Nome completo do avaliador',
                        'example': 'João Silva Santos'
                    },
                    'siape_or_cpf': {
                        'type': 'string',
                        'description': 'SIAPE ou CPF do avaliador',
                        'example': '11122233344'
                    },
                    'birthdate': {
                        'type': 'string',
                        'description': 'Data de nascimento no formato DDMMAAAA',
                        'example': '15031990'
                    },
                    'area': {
                        'type': 'string',
                        'description': 'Área de conhecimento do avaliador',
                        'example': 'Computação'
                    },
                    'subareas': {
                        'type': 'string',
                        'description': 'Subáreas de interesse separadas por ponto e vírgula',
                        'example': 'Inteligência Artificial;Machine Learning'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Avaliador cadastrado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
                        'type': 'string',
                        'description': 'Mensagem de sucesso',
                        'example': 'Avaliador cadastrado com sucesso!'
                    }
                }
            }
        },
        400: {
            'description': 'Dados inválidos',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
                        'type': 'string',
                        'description': 'Mensagem de erro'
                    }
                }
            }
        },
        409: {
            'description': 'SIAPE/CPF já cadastrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {
                        'type': 'string',
                        'description': 'Mensagem de erro'
                    }
                }
            }
        }
    }
})
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
