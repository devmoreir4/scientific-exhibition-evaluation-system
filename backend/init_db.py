from app import create_app
from app.extensions import db
from app.models import Evaluator, Work, Admin
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # TODO: coletar todos as areas e subareas
    # TODO: coletar todos os trabalhos
    # TODO: coletar todos os avaliadores
    # TODO: feature de importação de trabalhos
    # TODO: feature de ler a ficha de avaliação OCR

    admin_login = os.getenv('ADMIN_LOGIN', 'admin')
    admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
    if not Admin.query.filter_by(login=admin_login).first():
        admin = Admin(
            name='Administrador',
            login=admin_login,
            password_hash=generate_password_hash(admin_password)
        )
        db.session.add(admin)

    # Criar avaliadores
    if not Evaluator.query.filter_by(siape_or_cpf='123456789').first():
        ped = Evaluator(
            name='Avaliador Pedagógico',
            siape_or_cpf='123456789',
            birthdate='01011980',
            area='Pedagógica',
            subareas='Sociedade, Educação'
        )
        db.session.add(ped)
    if not Evaluator.query.filter_by(siape_or_cpf='98765432100').first():
        tec = Evaluator(
            name='Avaliador Técnico',
            siape_or_cpf='98765432100',
            birthdate='02021985',
            area='Computação',
            subareas='Robótica, IA'
        )
        db.session.add(tec)

    # Criar trabalhos
    works = [
        Work(
            title='Análise Preditiva de Evasão Escolar com IA',
            authors='Ana B. Silva, Maria C. Santos',
            advisor='Prof. Dr. João Silva',
            type='poster_banner',
            area='Computação',
            subarea='IA'
        ),
        Work(
            title='Robô Seguidor de Linha Otimizado',
            authors='Carlos de Souza, Pedro Oliveira',
            advisor='Prof. Dr. Roberto Lima',
            type='oral_presentation',
            area='Computação',
            subarea='Robótica'
        ),
        Work(
            title='Horta Urbana Sustentável Automatizada',
            authors='Mariana Costa, Luiza Ferreira',
            advisor='Prof. Dra. Ana Paula Costa',
            type='poster_banner',
            area='Sustentabilidade',
            subarea='Sustentabilidade'
        ),
        Work(
            title='Impacto das Fake News na Sociedade',
            authors='João Pereira',
            advisor='Prof. Dr. Marcos Almeida',
            type='oral_presentation',
            area='Pedagógica',
            subarea='Sociedade'
        ),
        Work(
            title='Síntese de Bioplástico a partir do Amido de Mandioca',
            authors='Fernanda Lima, Rafael Santos, Juliana Costa',
            advisor='Prof. Dra. Carla Mendes',
            type='poster_banner',
            area='Química',
            subarea='Polímeros'
        )
    ]
    db.session.add_all(works)
    db.session.commit()
    print('Initial tables and data created successfully!') 