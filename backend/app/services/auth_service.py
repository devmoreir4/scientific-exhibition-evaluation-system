from app.models import Evaluator, Admin
from app.extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token
import re


def validate_evaluator_registration(data):
    errors = []

    name = data.get('name', '').strip()
    siape_or_cpf = data.get('siape_or_cpf', '').strip()
    birthdate = data.get('birthdate', '').strip()
    area = data.get('area', '').strip()
    subareas = data.get('subareas', '').strip()

    if not all([name, siape_or_cpf, birthdate, area]):
        errors.append('Dados obrigatórios faltando')
        return False, errors

    if not re.fullmatch(r'\d{8}', birthdate):
        errors.append('A data de nascimento deve conter 8 dígitos (DDMMAAAA)')
        return False, errors

    existing_evaluator = Evaluator.query.filter_by(siape_or_cpf=siape_or_cpf).first()
    if existing_evaluator:
        errors.append('SIAPE ou CPF já cadastrado')
        return False, errors

    return True, {
        'name': name,
        'siape_or_cpf': siape_or_cpf,
        'birthdate': birthdate,
        'area': area,
        'subareas': subareas
    }


def create_evaluator(validated_data):
    evaluator = Evaluator(
        name=validated_data['name'],
        siape_or_cpf=validated_data['siape_or_cpf'],
        birthdate=validated_data['birthdate'],
        area=validated_data['area'],
        subareas=validated_data['subareas']
    )

    db.session.add(evaluator)
    db.session.commit()

    return evaluator


def authenticate_evaluator(siape_or_cpf, password):
    if not siape_or_cpf or not password:
        return None, 'Credenciais são obrigatórias'

    siape_or_cpf = siape_or_cpf.strip()

    evaluator = Evaluator.query.filter(Evaluator.siape_or_cpf.ilike(siape_or_cpf)).first()

    if not evaluator:
        return None, 'Credenciais inválidas'

    password_valid = False

    if evaluator.password_hash:
        password_valid = check_password_hash(evaluator.password_hash, password)
    else:
        password_valid = (evaluator.birthdate == password)

    if not password_valid:
        return None, 'Credenciais inválidas'

    return evaluator, None


def authenticate_admin(login, password):
    if not login or not password:
        return None, 'Credenciais são obrigatórias'

    admin = Admin.query.filter_by(login=login).first()

    if not admin or not check_password_hash(admin.password_hash, password):
        return None, 'Credenciais inválidas'

    return admin, None


def generate_access_token(user, role):
    if role == 'evaluator':
        identity = str(user.id)
    elif role == 'admin':
        identity = f'admin:{user.id}'
    else:
        raise ValueError('Tipo de usuário inválido')

    return create_access_token(identity=identity)


def validate_password_change(evaluator, current_password, new_password):
    errors = []

    if not current_password or not new_password:
        errors.append('Senha atual e nova senha são obrigatórias')
        return False, errors

    if len(new_password) < 6:
        errors.append('A nova senha deve ter pelo menos 6 caracteres')
        return False, errors

    current_password_valid = False

    if evaluator.password_hash:
        current_password_valid = check_password_hash(evaluator.password_hash, current_password)
    else:
        current_password_valid = (evaluator.birthdate == current_password)

    if not current_password_valid:
        errors.append('Senha atual incorreta')
        return False, errors

    return True, None


def change_evaluator_password(evaluator, new_password):
    evaluator.password_hash = generate_password_hash(new_password)
    db.session.commit()
    return evaluator


def validate_siape_or_cpf(siape_or_cpf):
    if not siape_or_cpf:
        return False, 'SIAPE ou CPF é obrigatório'

    siape_or_cpf = siape_or_cpf.strip()

    clean_value = re.sub(r'[^\d]', '', siape_or_cpf)

    if len(clean_value) == 7:
        if not clean_value.isdigit():
            return False, 'SIAPE deve conter apenas números'
        return True, 'SIAPE válido'

    elif len(clean_value) == 11:
        if not clean_value.isdigit():
            return False, 'CPF deve conter apenas números'

        if clean_value == clean_value[0] * 11:
            return False, 'CPF inválido'

        return True, 'CPF válido'

    else:
        return False, 'SIAPE deve ter 7 dígitos ou CPF deve ter 11 dígitos'


def validate_birthdate(birthdate):
    if not birthdate:
        return False, 'Data de nascimento é obrigatória'

    birthdate = birthdate.strip()

    if not re.fullmatch(r'\d{8}', birthdate):
        return False, 'Data de nascimento deve ter 8 dígitos (DDMMAAAA)'

    day = birthdate[:2]
    month = birthdate[2:4]
    year = birthdate[4:]

    if not (1 <= int(day) <= 31):
        return False, 'Dia inválido na data de nascimento'

    if not (1 <= int(month) <= 12):
        return False, 'Mês inválido na data de nascimento'

    if not (1900 <= int(year) <= 2020):
        return False, 'Ano inválido na data de nascimento'

    return True, 'Data de nascimento válida'


def check_evaluator_exists(siape_or_cpf):
    return Evaluator.query.filter_by(siape_or_cpf=siape_or_cpf.strip()).first() is not None


def get_evaluator_by_id(evaluator_id):
    return Evaluator.query.get(evaluator_id)


def get_admin_by_id(admin_id):
    return Admin.query.get(admin_id)


def validate_login_credentials(data, user_type='evaluator'):
    errors = []

    if user_type == 'evaluator':
        siape_or_cpf = data.get('siape_or_cpf', '').strip()
        password = data.get('password', '')

        if not siape_or_cpf:
            errors.append('SIAPE ou CPF é obrigatório')

        if not password:
            errors.append('Senha é obrigatória')

        return len(errors) == 0, errors

    elif user_type == 'admin':
        login = data.get('login', '').strip()
        password = data.get('password', '')

        if not login:
            errors.append('Login é obrigatório')

        if not password:
            errors.append('Senha é obrigatória')

        return len(errors) == 0, errors

    else:
        return False, ['Tipo de usuário inválido']


def is_password_strong(password):
    if len(password) < 6:
        return False, 'Senha deve ter pelo menos 6 caracteres'

    return True, 'Senha válida'


def sanitize_evaluator_data(data):
    return {
        'name': data.get('name', '').strip().title(),
        'siape_or_cpf': data.get('siape_or_cpf', '').strip(),
        'birthdate': data.get('birthdate', '').strip(),
        'area': data.get('area', '').strip(),
        'subareas': data.get('subareas', '').strip()
    }
