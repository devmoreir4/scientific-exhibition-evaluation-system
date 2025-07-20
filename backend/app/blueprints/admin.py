from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.services.distribution_service import distribute_works
from app.models import Evaluator, Work
from app.extensions import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/works/distribute', methods=['POST'])
@jwt_required()
def distribute():
    try:
        distribute_works()
        return jsonify({'msg': 'Distribuição realizada com sucesso!'}), 200
    except Exception as e:
        return jsonify({'msg': f'Erro na distribuição: {str(e)}'}), 500

# --- Administração de usuários ---
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    users = Evaluator.query.all()
    return jsonify({'users': [
        {'id': u.id, 'name': u.name, 'email': u.email, 'type': u.type, 'carga': u.carga}
        for u in users
    ]}), 200

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = Evaluator.query.get(user_id)
    if not user:
        return jsonify({'msg': 'Usuário não encontrado.'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': 'Usuário removido com sucesso!'}), 200

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = Evaluator.query.get(user_id)
    if not user:
        return jsonify({'msg': 'Usuário não encontrado.'}), 404
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.type = data.get('type', user.type)
    db.session.commit()
    return jsonify({'msg': 'Usuário atualizado com sucesso!'}), 200

# --- Administração de trabalhos ---
@admin_bp.route('/works', methods=['GET'])
@jwt_required()
def list_works():
    works = Work.query.all()
    return jsonify({'works': [
        {'id': w.id, 'title': w.title, 'author': w.author, 'area': w.area, 'subarea': w.subarea, 'abstract': w.abstract, 'has_technical_student': w.has_technical_student, 'has_prototype': w.has_prototype}
        for w in works
    ]}), 200

@admin_bp.route('/works/<int:work_id>', methods=['DELETE'])
@jwt_required()
def delete_work(work_id):
    work = Work.query.get(work_id)
    if not work:
        return jsonify({'msg': 'Trabalho não encontrado.'}), 404
    db.session.delete(work)
    db.session.commit()
    return jsonify({'msg': 'Trabalho removido com sucesso!'}), 200

@admin_bp.route('/works/<int:work_id>', methods=['PUT'])
@jwt_required()
def update_work(work_id):
    work = Work.query.get(work_id)
    if not work:
        return jsonify({'msg': 'Trabalho não encontrado.'}), 404
    data = request.get_json()
    work.title = data.get('title', work.title)
    work.author = data.get('author', work.author)
    work.area = data.get('area', work.area)
    work.subarea = data.get('subarea', work.subarea)
    work.abstract = data.get('abstract', work.abstract)
    work.has_technical_student = data.get('has_technical_student', work.has_technical_student)
    work.has_prototype = data.get('has_prototype', work.has_prototype)
    db.session.commit()
    return jsonify({'msg': 'Trabalho atualizado com sucesso!'}), 200 