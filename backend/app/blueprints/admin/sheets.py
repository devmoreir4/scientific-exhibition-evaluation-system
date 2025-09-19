from . import admin_bp
from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from app.services.ai_service import process_sheet_image_ai
from app.services.evaluation_service import validate_manual_evaluation_data, create_manual_evaluation
import os
from .misc import admin_required


def get_upload_folder():
    folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(folder, exist_ok=True)
    return folder


def get_next_evaluation_number():
    upload_folder = get_upload_folder()
    existing = [f for f in os.listdir(
        upload_folder) if f.startswith('evaluation_')]
    nums = [int(f.split('_')[1].split('.')[0])
            for f in existing if f.split('_')[1].split('.')[0].isdigit()]
    return max(nums, default=0) + 1


@admin_bp.route('/sheets/process-ai', methods=['POST'])
@jwt_required()
@admin_required
@swag_from({
    'tags': ['Admin - Fichas IA'],
    'summary': 'Processar ficha com IA',
    'description': 'Processa uma imagem de ficha de avaliação usando IA para extrair as notas automaticamente',
    'security': [{'Bearer': []}],
    'consumes': ['multipart/form-data'],
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'Imagem da ficha de avaliação (JPG, PNG, etc.)'
        }
    ],
    'responses': {
        200: {
            'description': 'Ficha processada com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string'},
                    'extracted_data': {
                        'type': 'object',
                        'properties': {
                            'criterion1': {'type': 'number'},
                            'criterion2': {'type': 'number'},
                            'criterion3': {'type': 'number'},
                            'criterion4': {'type': 'number'},
                            'criterion5': {'type': 'number'},
                            'evaluator_info': {'type': 'string'},
                            'work_info': {'type': 'string'}
                        }
                    },
                    'image_path': {'type': 'string'}
                }
            }
        },
        400: {'description': 'Arquivo inválido ou não enviado'},
        500: {'description': 'Erro no processamento da IA'},
        403: {'description': 'Acesso negado'}
    }
})
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
@swag_from({
    'tags': ['Admin - Fichas IA'],
    'summary': 'Confirmar dados extraídos',
    'description': 'Confirma e salva os dados extraídos da ficha (manual ou após processamento IA)',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['work_id', 'evaluator_id', 'scores'],
                'properties': {
                    'work_id': {'type': 'integer', 'example': 1},
                    'evaluator_id': {'type': 'integer', 'example': 1},
                    'scores': {
                        'type': 'array',
                        'items': {'type': 'number', 'minimum': 1, 'maximum': 5},
                        'minItems': 5,
                        'maxItems': 5,
                        'example': [4, 5, 3, 4, 5],
                        'description': 'Array com as 5 notas dos critérios'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Avaliação manual salva com sucesso',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string', 'example': 'Avaliação manual salva com sucesso!'}
                }
            }
        },
        400: {'description': 'Dados inválidos'},
        404: {'description': 'Trabalho ou avaliador não encontrado'},
        403: {'description': 'Acesso negado'}
    }
})
def confirm_sheet():
    data = request.get_json()

    is_valid, error_message = validate_manual_evaluation_data(data)

    if not is_valid:
        return jsonify({'msg': error_message}), 400 if 'obrigatórios' in error_message else 404

    work_id = data.get('work_id')
    evaluator_id = data.get('evaluator_id')
    scores = data.get('scores')

    create_manual_evaluation(work_id, evaluator_id, scores)

    return jsonify({'msg': 'Avaliação manual salva com sucesso!'}), 201
