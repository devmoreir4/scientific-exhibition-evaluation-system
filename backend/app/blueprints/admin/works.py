from . import admin_bp
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Work, Evaluator
from app.extensions import db
from app.services.csv_importer_service import import_works_from_csv
import io

@admin_bp.route('/works', methods=['GET'])
@jwt_required()
def list_works():
    works = Work.query.all()
    return jsonify({'works': [
        {'id': w.id, 'title': w.title, 'authors': w.authors, 'advisor': w.advisor, 'type': w.type, 'area': w.area, 'subarea': w.subarea}
        for w in works
    ]}), 200

@admin_bp.route('/works/distributions', methods=['GET'])
@jwt_required()
def list_work_distributions():
    """Lista todas as distribuições de trabalhos com seus avaliadores"""
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
    work.authors = data.get('authors', work.authors)
    work.advisor = data.get('advisor', work.advisor)
    work.type = data.get('type', work.type)
    work.area = data.get('area', work.area)
    work.subarea = data.get('subarea', work.subarea)
    db.session.commit()
    return jsonify({'msg': 'Trabalho atualizado com sucesso!'}), 200 