from . import auth_bp
from flask import request, jsonify
from flasgger import swag_from
from app.services.auth_service import (
    authenticate_evaluator, authenticate_admin,
    generate_access_token, validate_login_credentials
)

@auth_bp.route('/token', methods=['POST'])
@swag_from({
    'tags': ['Autenticação'],
    'summary': 'Login de avaliador',
    'description': 'Realiza login de avaliador e retorna token JWT',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['siape_or_cpf', 'password'],
                'properties': {
                    'siape_or_cpf': {
                        'type': 'string',
                        'description': 'SIAPE ou CPF do avaliador',
                        'example': '123456789'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Senha do avaliador (data de nascimento DDMMAAAA)',
                        'example': '01011980'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login realizado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'access_token': {
                        'type': 'string',
                        'description': 'Token JWT para autenticação'
                    },
                    'role': {
                        'type': 'string',
                        'description': 'Tipo de usuário',
                        'example': 'evaluator'
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
        401: {
            'description': 'Credenciais inválidas',
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
def login():
    data = request.get_json()

    # Validate login credentials
    is_valid, errors = validate_login_credentials(data, 'evaluator')
    if not is_valid:
        return jsonify({'msg': '; '.join(errors)}), 400

    # Authenticate evaluator
    siape_or_cpf = data.get('siape_or_cpf')
    password = data.get('password')

    evaluator, error_msg = authenticate_evaluator(siape_or_cpf, password)

    if not evaluator:
        return jsonify({'msg': error_msg}), 401

    # Generate access token
    access_token = generate_access_token(evaluator, 'evaluator')

    return jsonify({'access_token': access_token, 'role': 'evaluator'}), 200

@auth_bp.route('/admin/token', methods=['POST'])
@swag_from({
    'tags': ['Autenticação'],
    'summary': 'Login de administrador',
    'description': 'Realiza login de administrador e retorna token JWT',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['login', 'password'],
                'properties': {
                    'login': {
                        'type': 'string',
                        'description': 'Login do administrador',
                        'example': 'admin'
                    },
                    'password': {
                        'type': 'string',
                        'description': 'Senha do administrador',
                        'example': 'admin123'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login realizado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'access_token': {
                        'type': 'string',
                        'description': 'Token JWT para autenticação'
                    },
                    'role': {
                        'type': 'string',
                        'description': 'Tipo de usuário',
                        'example': 'admin'
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
        401: {
            'description': 'Credenciais inválidas',
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
def login_admin():
    data = request.get_json()

    # Validate login credentials
    is_valid, errors = validate_login_credentials(data, 'admin')
    if not is_valid:
        return jsonify({'msg': '; '.join(errors)}), 400

    # Authenticate admin
    login = data.get('login')
    password = data.get('password')

    admin, error_msg = authenticate_admin(login, password)

    if not admin:
        return jsonify({'msg': error_msg}), 401

    # Generate access token
    access_token = generate_access_token(admin, 'admin')

    return jsonify({'access_token': access_token, 'role': 'admin'}), 200
