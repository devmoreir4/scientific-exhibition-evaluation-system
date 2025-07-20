from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Evaluator, Work, Evaluation
from app.extensions import db

evaluator_bp = Blueprint('evaluator', __name__)

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

@evaluator_bp.route('/evaluations', methods=['POST'])
@jwt_required()
def submit_evaluation():
    evaluator_id = int(get_jwt_identity())
    data = request.get_json()
    work_id = data.get('work_id')
    criteria = [data.get(f'criterion{i}') for i in range(1, 6)]
    comments = data.get('comments', '')

    # Validação de dados obrigatórios
    if not work_id or not all(c is not None for c in criteria):
        return jsonify({'msg': 'Dados obrigatórios faltando.'}), 400

    # Validação de faixa de notas (1 a 5)
    for idx, c in enumerate(criteria, 1):
        if not isinstance(c, int) or c < 1 or c > 5:
            return jsonify({'msg': f'Critério {idx} deve ser um número inteiro de 1 (Ruim) a 5 (Excelente).'}), 400

    work = Work.query.get(work_id)
    if not work:
        return jsonify({'msg': 'Trabalho não encontrado.'}), 404

    # Verifica se o avaliador está atribuído ao trabalho
    evaluator = Evaluator.query.get(evaluator_id)
    if work not in evaluator.works:
        return jsonify({'msg': 'Você não está autorizado a avaliar este trabalho.'}), 403

    # Impedir avaliação duplicada
    existing = Evaluation.query.filter_by(evaluator_id=evaluator_id, work_id=work_id).first()
    if existing:
        return jsonify({'msg': 'Você já avaliou este trabalho.'}), 409

    evaluation = Evaluation(
        criterion1=criteria[0],
        criterion2=criteria[1],
        criterion3=criteria[2],
        criterion4=criteria[3],
        criterion5=criteria[4],
        comments=comments,
        evaluator_id=evaluator_id,
        work_id=work_id
    )
    db.session.add(evaluation)
    db.session.commit()
    return jsonify({'msg': 'Avaliação registrada com sucesso!'}), 201

@evaluator_bp.route('/evaluations/mine', methods=['GET'])
@jwt_required()
def list_my_evaluations():
    evaluator_id = int(get_jwt_identity())
    evaluations = Evaluation.query.filter_by(evaluator_id=evaluator_id).all()
    result = []
    for ev in evaluations:
        result.append({
            'id': ev.id,
            'work_id': ev.work_id,
            'criterion1': ev.criterion1,
            'criterion2': ev.criterion2,
            'criterion3': ev.criterion3,
            'criterion4': ev.criterion4,
            'criterion5': ev.criterion5,
            'comments': ev.comments
        })
    return jsonify({'evaluations': result}), 200

@evaluator_bp.route('/evaluations/work/<int:work_id>', methods=['GET'])
@jwt_required()
def list_evaluations_for_work(work_id):
    evaluations = Evaluation.query.filter_by(work_id=work_id).all()
    result = []
    for ev in evaluations:
        result.append({
            'id': ev.id,
            'evaluator_id': ev.evaluator_id,
            'criterion1': ev.criterion1,
            'criterion2': ev.criterion2,
            'criterion3': ev.criterion3,
            'criterion4': ev.criterion4,
            'criterion5': ev.criterion5,
            'comments': ev.comments
        })
    return jsonify({'evaluations': result}), 200 