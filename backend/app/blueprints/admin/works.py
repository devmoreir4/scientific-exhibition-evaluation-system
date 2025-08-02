from . import admin_bp
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Work, Evaluator
from app.extensions import db
from app.services.csv_importer_service import import_works_from_csv
import io
from app.models import Evaluation
from .misc import admin_required

@admin_bp.route('/works', methods=['GET'])
@jwt_required()
@admin_required
def list_works():
    works = Work.query.all()
    return jsonify({'works': [
        {'id': w.id, 'title': w.title, 'authors': w.authors, 'advisor': w.advisor, 'type': w.type, 'area': w.area, 'subarea': w.subarea}
        for w in works
    ]}), 200

@admin_bp.route('/works/distributions', methods=['GET'])
@jwt_required()
@admin_required
def list_work_distributions():
    works = Work.query.all()
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
                'carga': evaluator.carga
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

    return jsonify({'distributions': distributions}), 200

@admin_bp.route('/works/import-csv', methods=['POST'])
@jwt_required()
@admin_required
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
def get_evaluation_progress():
    works = Work.query.all()
    evaluations = Evaluation.query.all()

    total_works = len(works)
    total_evaluations = len(evaluations)

    works_with_evaluations = {}
    for work in works:
        work_evaluations = [e for e in evaluations if e.work_id == work.id]
        evaluated_evaluator_ids = [e.evaluator_id for e in work_evaluations]

        # identificar avaliadores que ainda não avaliaram
        pending_evaluators = []
        for evaluator in work.evaluators:
            if evaluator.id not in evaluated_evaluator_ids:
                pending_evaluators.append({
                    'id': evaluator.id,
                    'name': evaluator.name,
                    'siape_or_cpf': evaluator.siape_or_cpf
                })

        works_with_evaluations[work.id] = {
            'work_id': work.id,
            'work_title': work.title,
            'work_area': work.area,
            'work_subarea': work.subarea,
            'total_evaluators': len(work.evaluators),
            'completed_evaluations': len(work_evaluations),
            'pending_evaluations': len(work.evaluators) - len(work_evaluations),
            'progress_percentage': round((len(work_evaluations) / len(work.evaluators)) * 100, 1) if work.evaluators else 0,
            'pending_evaluators': pending_evaluators
        }

    # estatísticas gerais
    total_expected_evaluations = sum(len(work.evaluators) for work in works)
    overall_progress = round((total_evaluations / total_expected_evaluations) * 100, 1) if total_expected_evaluations > 0 else 0

    return jsonify({
        'overall_stats': {
            'total_works': total_works,
            'total_evaluations': total_evaluations,
            'total_expected_evaluations': total_expected_evaluations,
            'overall_progress': overall_progress
        },
        'works_progress': list(works_with_evaluations.values())
    }), 200

@admin_bp.route('/works/podium', methods=['GET'])
@jwt_required()
@admin_required
def get_works_podium():
    works = Work.query.all()
    evaluations = Evaluation.query.all()

    works_by_area = {}
    for work in works:
        if work.area not in works_by_area:
            works_by_area[work.area] = []
        works_by_area[work.area].append(work)

    podium_data = {}

    for area, area_works in works_by_area.items():
        # calcular média de cada trabalho na área
        works_with_scores = []

        for work in area_works:
            work_evaluations = [e for e in evaluations if e.work_id == work.id]

            if work_evaluations:
                # calcular média dos critérios
                total_score = 0
                for evaluation in work_evaluations:
                    total_score += (evaluation.criterion1 + evaluation.criterion2 +
                                  evaluation.criterion3 + evaluation.criterion4 +
                                  evaluation.criterion5)

                average_score = total_score / (len(work_evaluations) * 5)

                works_with_scores.append({
                    'work_id': work.id,
                    'work_title': work.title,
                    'work_authors': work.authors,
                    'work_advisor': work.advisor,
                    'work_type': work.type,
                    'work_subarea': work.subarea,
                    'evaluations_count': len(work_evaluations),
                    'average_score': round(average_score, 2),
                    'total_score': total_score
                })

        works_with_scores.sort(key=lambda x: x['average_score'], reverse=True)
        top_3 = works_with_scores[:3]

        podium_data[area] = {
            'area_name': area,
            'total_works': len(area_works),
            'evaluated_works': len(works_with_scores),
            'podium': top_3
        }

    return jsonify({
        'podium_data': podium_data
    }), 200
