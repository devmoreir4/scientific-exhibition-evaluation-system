from . import admin_bp
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.distribution_service import distribute_works

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
        distribute_works()
        return jsonify({'msg': 'Distribuição realizada com sucesso!'}), 200
    except Exception as e:
        return jsonify({'msg': f'Erro na distribuição: {str(e)}'}), 500 