from app import create_app
from app.extensions import db
from app.models import Evaluator
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    evaluators = [
        Evaluator(
            name='Prof. Dr. João Silva',
            siape_or_cpf='123456789',
            birthdate='01011980',
            area='Ciências Exatas e da Terra e Engenharias',
            subareas='Tecnologias da Informação e Programação; Robótica, Automação e Eletrônica'
        ),
        Evaluator(
            name='Prof. Dra. Maria Santos',
            siape_or_cpf='987654321',
            birthdate='15021982',
            area='Ciências Biológicas e Ciências da Saúde',
            subareas='Biotecnologia e Microbiologia; Saúde Coletiva e Educação em Saúde'
        ),
        Evaluator(
            name='Prof. Dr. Carlos Mendes',
            siape_or_cpf='456789123',
            birthdate='20031985',
            area='Ciências Agrárias',
            subareas='Agricultura e Sustentabilidade no Campo; Agroindústria e Alimentos'
        ),
        Evaluator(
            name='Prof. Dra. Ana Paula Costa',
            siape_or_cpf='789123456',
            birthdate='10041978',
            area='Ciências Sociais Aplicadas e Ciências Humanas',
            subareas='Educação, Cidadania e Direitos Humanos; Gestão, Empreendedorismo e Economia'
        ),
        Evaluator(
            name='Prof. Dr. Roberto Lima',
            siape_or_cpf='321654987',
            birthdate='05051983',
            area='Linguística, Letras e Artes',
            subareas='Língua Portuguesa e Produção Textual; Literatura, Leitura e Narrativas'
        ),
        Evaluator(
            name='Prof. Dra. Beatriz Ferreira',
            siape_or_cpf='654987321',
            birthdate='25061979',
            area='Ciências Biológicas e Ciências da Saúde',
            subareas='Ecologia e Conservação; Nutrição, Enfermagem e Bem-estar'
        ),
        Evaluator(
            name='Prof. Dr. Ricardo Almeida',
            siape_or_cpf='147258369',
            birthdate='12071981',
            area='Ciências Exatas e da Terra e Engenharias',
            subareas='Engenharia e Energias Renováveis; Geociências e Sustentabilidade Ambiental'
        ),
        Evaluator(
            name='Prof. Dra. Patricia Oliveira',
            siape_or_cpf='963852741',
            birthdate='08081984',
            area='Ciências Sociais Aplicadas e Ciências Humanas',
            subareas='História, Filosoa e Sociologia; Geografia e Estudos Regionais'
        ),
        # avaliadores pedagógicos
        Evaluator(
            name='Prof. Dr. José Pedagógico',
            siape_or_cpf='111222333',
            birthdate='15031975',
            area='Pedagógica',
            subareas='Educação, Cidadania e Direitos Humanos; Gestão, Empreendedorismo e Economia'
        ),
        Evaluator(
            name='Prof. Dra. Sandra Pedagógica',
            siape_or_cpf='444555666',
            birthdate='22081976',
            area='Pedagógica',
            subareas='Educação, Cidadania e Direitos Humanos; Comunicação, Informação e Cultura Digital'
        ),
        Evaluator(
            name='Prof. Dr. Paulo Pedagógico',
            siape_or_cpf='777888999',
            birthdate='18051977',
            area='Pedagógica',
            subareas='História, Filosoa e Sociologia; Geografia e Estudos Regionais'
        ),
        Evaluator(
            name='Prof. Dra. Fernanda Pedagógica',
            siape_or_cpf='000111222',
            birthdate='30091974',
            area='Pedagógica',
            subareas='Língua Portuguesa e Produção Textual; Literatura, Leitura e Narrativas'
        )
    ]

    # Verificar se já existem avaliadores para não duplicar
    existing_count = Evaluator.query.count()
    if existing_count == 0:
        for evaluator in evaluators:
            db.session.add(evaluator)
        db.session.commit()
        print(f'{len(evaluators)} avaliadores criados com sucesso!')
    else:
        print(f'Já existem {existing_count} avaliadores no sistema. Nenhum avaliador foi criado.')

    print('Script teste de inicialização de avaliadores concluído!')
