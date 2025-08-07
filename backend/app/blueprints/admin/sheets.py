from . import admin_bp
from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.ai_service import process_sheet_image_ai
from app.models import Evaluation, Evaluator, Work
from app.extensions import db
import os
from .misc import admin_required


def get_upload_folder():
    folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(folder, exist_ok=True)
    return folder

def get_next_evaluation_number():
    upload_folder = get_upload_folder()
    existing = [f for f in os.listdir(upload_folder) if f.startswith('evaluation_')]
    nums = [int(f.split('_')[1].split('.')[0]) for f in existing if f.split('_')[1].split('.')[0].isdigit()]
    return max(nums, default=0) + 1

@admin_bp.route('/sheets/process-ai', methods=['POST'])
@jwt_required()
@admin_required
def process_sheet_ai():
    if 'file' not in request.files:
        return jsonify({'msg': 'Arquivo não enviado.'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'msg': 'Nenhum arquivo selecionado.'}), 400
    image_bytes = file.read()
    if not image_bytes:
        return jsonify({'msg': 'Arquivo enviado está vazio ou corrompido.'}), 400
    try:
        ext = os.path.splitext(file.filename or 'sheet.jpg')[1]
        numero = get_next_evaluation_number()
        filename = f"evaluation_{numero}{ext}"
        upload_folder = get_upload_folder()
        save_path = os.path.join(upload_folder, filename)
        with open(save_path, 'wb') as f:
            f.write(image_bytes)
        result = process_sheet_image_ai(image_bytes)
        result['saved_image'] = filename
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'msg': str(e)}), 400
    except Exception as e:
        return jsonify({'msg': f'Erro interno: {str(e)}'}), 500

@admin_bp.route('/sheets/confirm', methods=['POST'])
@jwt_required()
@admin_required
def confirm_sheet():
    data = request.get_json()
    work_id = data.get('work_id')
    scores = data.get('scores')
    evaluator_id = data.get('evaluator_id')

    if not work_id or not evaluator_id or not scores or len(scores) != 5:
        return jsonify({'msg': 'Dados obrigatórios faltando.'}), 400

    evaluator = Evaluator.query.get(evaluator_id)
    if not evaluator:
        return jsonify({'msg': 'Avaliador não encontrado.'}), 404

    work = Work.query.get(work_id)
    if not work:
        return jsonify({'msg': 'Trabalho não encontrado.'}), 404

    works_with_evaluators = Work.query.filter(Work.evaluators.any()).count()
    if works_with_evaluators == 0:
        return jsonify({'msg': 'Nenhum trabalho foi distribuído ainda.'}), 400

    if evaluator not in work.evaluators:
        return jsonify({'msg': 'Este avaliador não foi atribuído para avaliar este trabalho.'}), 403

    existing_evaluation = Evaluation.query.filter_by(
        evaluator_id=evaluator_id,
        work_id=work_id
    ).first()

    if existing_evaluation:
        return jsonify({'msg': 'Este avaliador já avaliou este trabalho.'}), 409

    for i, score in enumerate(scores):
        if not isinstance(score, (int, float)) or score < 1 or score > 5:
            return jsonify({'msg': f'Critério {i+1} deve ser um número entre 1 e 5.'}), 400

    evaluation = Evaluation(
        criterion1=scores[0],
        criterion2=scores[1],
        criterion3=scores[2],
        criterion4=scores[3],
        criterion5=scores[4],
        method='manual_validated',
        evaluator_id=evaluator_id,
        work_id=work_id
    )
    db.session.add(evaluation)
    db.session.commit()
    return jsonify({'msg': 'Avaliação manual salva com sucesso!'}), 201
