from . import admin_bp
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
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
def get_areas():
    """Retorna todas as áreas disponíveis"""
    try:
        areas = get_all_areas()
        return jsonify({'areas': areas}), 200
    except Exception as e:
        return jsonify({'msg': f'Erro ao buscar áreas: {str(e)}'}), 500

@admin_bp.route('/areas/<area>/subareas', methods=['GET'])
@jwt_required()
@admin_required
def get_subareas(area):
    """Retorna as subáreas de uma área específica"""
    try:
        if area == 'Pedagógica':
            # Área pedagógica pode ter acesso a todas as subáreas
            subareas = get_all_subareas()
        else:
            subareas = get_subareas_by_area(area)

        return jsonify({'subareas': subareas}), 200
    except Exception as e:
        return jsonify({'msg': f'Erro ao buscar subáreas: {str(e)}'}), 500
