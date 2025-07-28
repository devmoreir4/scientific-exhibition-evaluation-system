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
            author='Ana B. Silva / Ciência da Computação / IFRJ',
            area='Computação',
            subarea='IA',
            abstract='Este trabalho utiliza algoritmos de inteligência artificial para prever a evasão de alunos.',
            has_technical_student=True,
            has_prototype=False
        ),
        Work(
            title='Robô Seguidor de Linha Otimizado',
            author='Carlos de Souza / Eng. de Controle e Automação / IFRJ',
            area='Computação',
            subarea='Robótica',
            abstract='Desenvolvimento de um robô seguidor de linha com sensor infravermelho e controle PID para otimização de percurso.',
            has_technical_student=True,
            has_prototype=True
        ),
        Work(
            title='Horta Urbana Sustentável Automatizada',
            author='Mariana Costa / Técnico em Meio Ambiente / IFRJ',
            area='Sustentabilidade',
            subarea='Sustentabilidade',
            abstract='Projeto de uma horta vertical para espaços urbanos com sistema de irrigação automatizado por umidade do solo.',
            has_technical_student=True,
            has_prototype=True
        ),
        Work(
            title='Impacto das Fake News na Sociedade',
            author='João Pereira / Licenciatura em Pedagogia / IFRJ',
            area='Pedagógica',
            subarea='Sociedade',
            abstract='Estudo sobre a percepção e o impacto da desinformação em comunidades escolares.',
            has_technical_student=False,
            has_prototype=False
        ),
        Work(
            title='Síntese de Bioplástico a partir do Amido de Mandioca',
            author='Fernanda Lima / Técnico em Química / IFRJ',
            area='Química',
            subarea='Polímeros',
            abstract='Desenvolvimento de um método de baixo custo para a síntese de plástico biodegradável utilizando amido de mandioca.',
            has_technical_student=True,
            has_prototype=True
        )
    ]
    db.session.add_all(works)
    db.session.commit()
    print('Initial tables and data created successfully!') 