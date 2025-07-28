from . import evaluator_bp
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Evaluator

@evaluator_bp.route('/works/assigned', methods=['GET'])
@jwt_required()
def get_assigned_works():
    evaluator = Evaluator.query.get(int(get_jwt_identity()))
    if not evaluator:
        return jsonify({'msg': 'Avaliador não encontrado.'}), 404
    works = [
        {
            'id': w.id,
            'title': w.title,
            'author': w.author,
            'area': w.area,
            'subarea': w.subarea,
            'abstract': w.abstract,
            'has_technical_student': w.has_technical_student,
            'has_prototype': w.has_prototype
        }
        for w in evaluator.works
    ]
    return jsonify({'works': works}), 200

@evaluator_bp.route('/works/<int:work_id>', methods=['GET'])
@jwt_required()
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
        'author': work.author,
        'area': work.area,
        'subarea': work.subarea,
        'abstract': work.abstract,
        'has_technical_student': work.has_technical_student,
        'has_prototype': work.has_prototype
    }}), 200 