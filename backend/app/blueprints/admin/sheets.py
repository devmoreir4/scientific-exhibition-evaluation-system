from . import admin_bp
from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.ai_service import process_sheet_image_ai
from app.services.evaluation_service import validate_manual_evaluation_data, create_manual_evaluation
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

    # Validar dados usando o service
    is_valid, error_message = validate_manual_evaluation_data(data)

    if not is_valid:
        return jsonify({'msg': error_message}), 400 if 'obrigatórios' in error_message else 404

    # Criar avaliação usando o service
    work_id = data.get('work_id')
    evaluator_id = data.get('evaluator_id')
    scores = data.get('scores')

    create_manual_evaluation(work_id, evaluator_id, scores)

    return jsonify({'msg': 'Avaliação manual salva com sucesso!'}), 201
