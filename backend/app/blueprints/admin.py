from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.distribution_service import distribute_works
from app.services.ocr_service import process_sheet_image
from app.models import Evaluator, Work, Evaluation
from app.extensions import db
import os

admin_bp = Blueprint('admin', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_next_evaluation_number():
    existing = [f for f in os.listdir(UPLOAD_FOLDER) if f.startswith('evaluation_')]
    nums = [int(f.split('_')[1].split('.')[0]) for f in existing if f.split('_')[1].split('.')[0].isdigit()]
    return max(nums, default=0) + 1

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
    """
    Distribuir trabalhos automaticamente entre avaliadores
    ---
    tags:
      - Administração
    security:
      - BearerAuth: []
    responses:
      200:
        description: Distribuição realizada com sucesso
      500:
        description: Erro na distribuição
      403:
        description: Acesso restrito a administradores
    """
    try:
        distribute_works()
        return jsonify({'msg': 'Distribuição realizada com sucesso!'}), 200
    except Exception as e:
        return jsonify({'msg': f'Erro na distribuição: {str(e)}'}), 500

# --- Administração de usuários ---
@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def list_users():
    """
    Listar todos os avaliadores
    ---
    tags:
      - Administração
    security:
      - BearerAuth: []
    responses:
      200:
        description: Lista de avaliadores
      403:
        description: Acesso restrito a administradores
    """
    users = Evaluator.query.all()
    return jsonify({'users': [
        {'id': u.id, 'name': u.name, 'siape_or_cpf': u.siape_or_cpf, 'birthdate': u.birthdate, 'area': u.area, 'subareas': u.subareas, 'carga': u.carga}
        for u in users
    ]}), 200

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    """
    Remover avaliador
    ---
    tags:
      - Administração
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: user_id
        schema:
          type: integer
        required: true
        description: ID do avaliador
    responses:
      200:
        description: Usuário removido com sucesso
      404:
        description: Usuário não encontrado
      403:
        description: Acesso restrito a administradores
    """
    user = Evaluator.query.get(user_id)
    if not user:
        return jsonify({'msg': 'Usuário não encontrado.'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': 'Usuário removido com sucesso!'}), 200

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    """
    Editar avaliador
    ---
    tags:
      - Administração
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: user_id
        schema:
          type: integer
        required: true
        description: ID do avaliador
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              siape_or_cpf:
                type: string
              birthdate:
                type: string
              area:
                type: string
              subareas:
                type: string
    responses:
      200:
        description: Usuário atualizado com sucesso
      404:
        description: Usuário não encontrado
      403:
        description: Acesso restrito a administradores
    """
    user = Evaluator.query.get(user_id)
    if not user:
        return jsonify({'msg': 'Usuário não encontrado.'}), 404
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.siape_or_cpf = data.get('siape_or_cpf', user.siape_or_cpf)
    user.birthdate = data.get('birthdate', user.birthdate)
    user.area = data.get('area', user.area)
    user.subareas = data.get('subareas', user.subareas)
    db.session.commit()
    return jsonify({'msg': 'Usuário atualizado com sucesso!'}), 200

# --- Administração de trabalhos ---
@admin_bp.route('/works', methods=['GET'])
@jwt_required()
@admin_required
def list_works():
    """
    Listar todos os trabalhos
    ---
    tags:
      - Administração
    security:
      - BearerAuth: []
    responses:
      200:
        description: Lista de trabalhos
      403:
        description: Acesso restrito a administradores
    """
    works = Work.query.all()
    return jsonify({'works': [
        {'id': w.id, 'title': w.title, 'author': w.author, 'area': w.area, 'subarea': w.subarea, 'abstract': w.abstract, 'has_technical_student': w.has_technical_student, 'has_prototype': w.has_prototype}
        for w in works
    ]}), 200

@admin_bp.route('/works/<int:work_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_work(work_id):
    """
    Remover trabalho
    ---
    tags:
      - Administração
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: work_id
        schema:
          type: integer
        required: true
        description: ID do trabalho
    responses:
      200:
        description: Trabalho removido com sucesso
      404:
        description: Trabalho não encontrado
      403:
        description: Acesso restrito a administradores
    """
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
    """
    Editar trabalho
    ---
    tags:
      - Administração
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: work_id
        schema:
          type: integer
        required: true
        description: ID do trabalho
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              title:
                type: string
              author:
                type: string
              area:
                type: string
              subarea:
                type: string
              abstract:
                type: string
              has_technical_student:
                type: boolean
              has_prototype:
                type: boolean
    responses:
      200:
        description: Trabalho atualizado com sucesso
      404:
        description: Trabalho não encontrado
      403:
        description: Acesso restrito a administradores
    """
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

@admin_bp.route('/sheets/process', methods=['POST'])
@jwt_required()
@admin_required
def process_sheet():
    """
    Processar imagem de ficha de avaliação (OCR/OMR) e salvar backup
    ---
    tags:
      - Administração
    security:
      - BearerAuth: []
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: file
        type: file
        required: true
        description: Imagem da ficha preenchida
    responses:
      200:
        description: Dados extraídos da ficha
    """
    if 'file' not in request.files:
        return jsonify({'msg': 'Arquivo não enviado.'}), 400
    file = request.files['file']
    image_bytes = file.read()
    # salvar imagem
    ext = os.path.splitext(file.filename or 'sheet.jpg')[1]
    numero = get_next_evaluation_number()
    filename = f"evaluation_{numero}{ext}"
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(save_path, 'wb') as f:
        f.write(image_bytes)
    # processar OCR/OMR
    result = process_sheet_image(image_bytes)
    result['saved_image'] = filename
    return jsonify(result), 200

@admin_bp.route('/sheets/confirm', methods=['POST'])
@jwt_required()
@admin_required
def confirm_sheet():
    """
    Confirmar e salvar avaliação manual validada
    ---
    tags:
      - Administração
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - work_id
              - evaluator_id
              - scores
            properties:
              work_id:
                type: integer
              evaluator_id:
                type: integer
                description: ID do avaliador
              scores:
                type: array
                items:
                  type: integer
    responses:
      201:
        description: Avaliação manual salva com sucesso
      400:
        description: Dados obrigatórios faltando
    """
    data = request.get_json()
    work_id = data.get('work_id')
    scores = data.get('scores')
    evaluator_id = data.get('evaluator_id')
    if not work_id or not evaluator_id or not scores or len(scores) != 5:
        return jsonify({'msg': 'Dados obrigatórios faltando.'}), 400
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