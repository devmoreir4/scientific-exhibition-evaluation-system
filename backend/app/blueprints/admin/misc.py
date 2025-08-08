from . import admin_bp
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from app.services.distribution_service import distribute_works
from app.models import DistributionControl
from app.services.areas_service import get_all_areas, get_subareas_by_area, get_all_subareas

def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if not (isinstance(identity, str) and identity.startswith('admin:')):
            return jsonify({'msg': 'Acesso restrito a administradores.'}), 403
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/works/distribute', methods=['POST'])
@jwt_required()
@admin_required
@swag_from({
    'tags': ['Admin - Distribuição'],
    'summary': 'Distribuir trabalhos',
    'description': 'Distribui automaticamente os trabalhos entre os avaliadores',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Distribuição realizada com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string', 'example': 'Distribuição realizada com sucesso!'},
                    'distributed': {'type': 'boolean', 'example': True}
                }
            }
        },
        409: {
            'description': 'Distribuição já foi realizada',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string'},
                    'already_distributed': {'type': 'boolean'}
                }
            }
        },
        500: {'description': 'Erro interno na distribuição'},
        403: {'description': 'Acesso negado'}
    }
})
def distribute():
    try:
        if DistributionControl.is_distributed():
            return jsonify({
                'msg': 'A distribuição de trabalhos já foi realizada!',
                'already_distributed': True
            }), 409

        distribute_works()

        identity = get_jwt_identity()
        admin_name = identity.replace('admin:', '') if identity.startswith('admin:') else identity

        DistributionControl.mark_as_distributed(admin_name)

        return jsonify({
            'msg': 'Distribuição realizada com sucesso!',
            'distributed': True
        }), 200
    except Exception as e:
        return jsonify({'msg': f'Erro na distribuição: {str(e)}'}), 500

@admin_bp.route('/works/distribution-status', methods=['GET'])
@jwt_required()
@admin_required
@swag_from({
    'tags': ['Admin - Distribuição'],
    'summary': 'Status da distribuição',
    'description': 'Verifica o status atual da distribuição de trabalhos',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Status da distribuição',
            'schema': {
                'type': 'object',
                'properties': {
                    'distributed': {'type': 'boolean'},
                    'distributed_at': {'type': 'string', 'format': 'date-time', 'description': 'Data da distribuição (se realizada)'},
                    'distributed_by': {'type': 'string', 'description': 'Administrador que realizou a distribuição'},
                    'msg': {'type': 'string'}
                }
            }
        },
        500: {'description': 'Erro interno'},
        403: {'description': 'Acesso negado'}
    }
})
def distribution_status():
    try:
        control = DistributionControl.query.first()

        if control and control.distributed:
            return jsonify({
                'distributed': True,
                'distributed_at': control.distributed_at.isoformat() if control.distributed_at else None,
                'distributed_by': control.distributed_by,
                'msg': 'Distribuição já foi realizada'
            }), 200
        else:
            return jsonify({
                'distributed': False,
                'msg': 'Distribuição ainda não foi realizada'
            }), 200
    except Exception as e:
        return jsonify({'msg': f'Erro ao verificar status: {str(e)}'}), 500

@admin_bp.route('/works/reset-distribution', methods=['POST'])
@jwt_required()
@admin_required
@swag_from({
    'tags': ['Admin - Distribuição'],
    'summary': 'Reset da distribuição (Emergência)',
    'description': 'Reseta completamente a distribuição de trabalhos - remove todas as avaliações e associações',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Reset realizado com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string'},
                    'distributed': {'type': 'boolean', 'example': False},
                    'actions_performed': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'description': 'Lista de ações executadas no reset'
                    }
                }
            }
        },
        500: {'description': 'Erro interno'},
        403: {'description': 'Acesso negado'}
    }
})
def reset_distribution():
    try:
        DistributionControl.reset_distribution()
        return jsonify({
            'msg': 'Reset de distribuições realizado com sucesso!',
            'distributed': False,
            'actions_performed': [
                'Controle de distribuição resetado',
                'Todas as avaliações removidas',
                'Associações trabalho-avaliador limpas',
                'Workload dos avaliadores zerado'
            ]
        }), 200
    except Exception as e:
        return jsonify({'msg': f'Erro ao resetar distribuição: {str(e)}'}), 500

@admin_bp.route('/areas', methods=['GET'])
@jwt_required()
@admin_required
@swag_from({
    'tags': ['Admin - Áreas'],
    'summary': 'Listar áreas',
    'description': 'Lista todas as áreas de conhecimento disponíveis',
    'security': [{'Bearer': []}],
    'responses': {
        200: {
            'description': 'Lista de áreas',
            'schema': {
                'type': 'object',
                'properties': {
                    'areas': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    }
                }
            }
        },
        403: {'description': 'Acesso negado'}
    }
})
def get_areas():
    try:
        areas = get_all_areas()
        return jsonify({'areas': areas}), 200
    except Exception as e:
        return jsonify({'msg': f'Erro ao buscar áreas: {str(e)}'}), 500

@admin_bp.route('/areas/<area>/subareas', methods=['GET'])
@jwt_required()
@admin_required
@swag_from({
    'tags': ['Admin - Áreas'],
    'summary': 'Listar subáreas por área',
    'description': 'Lista todas as subáreas de uma área específica',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'area',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Nome da área (ex: Computação, Química, Pedagógica)'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de subáreas',
            'schema': {
                'type': 'object',
                'properties': {
                    'subareas': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    }
                }
            }
        },
        500: {'description': 'Erro interno'},
        403: {'description': 'Acesso negado'}
    }
})
def get_subareas(area):
    try:
        if area == 'Pedagógica':
            subareas = get_all_subareas()
        else:
            subareas = get_subareas_by_area(area)

        return jsonify({'subareas': subareas}), 200
    except Exception as e:
        return jsonify({'msg': f'Erro ao buscar subáreas: {str(e)}'}), 500
