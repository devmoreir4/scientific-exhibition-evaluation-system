import pandas as pd
from app.models import Work
from app.extensions import db

# Mapeamento de áreas e subáreas
VALID_AREAS = {
    'Ciências Agrárias',
    'Ciências Biológicas e Ciências da Saúde',
    'Ciências Exatas e da Terra e Engenharias',
    'Ciências Sociais Aplicadas e Ciências Humanas',
    'Linguística, Letras e Artes'
}

VALID_SUBAREAS = {
    # Ciências Agrárias
    'Agricultura e Sustentabilidade no Campo',
    'Zootecnia e Produção Animal',
    'Agroindústria e Alimentos',
    'Recursos Naturais e Meio Ambiente Rural',
    'Tecnologias e Processos Agrícolas',

    # Ciências Biológicas e Ciências da Saúde
    'Biotecnologia e Microbiologia',
    'Ecologia e Conservação',
    'Saúde Coletiva e Educação em Saúde',
    'Nutrição, Enfermagem e Bem-estar',
    'Práticas Integrativas e Promoção da Saúde',

    # Ciências Exatas e da Terra e Engenharias
    'Matemática, Física e Química Aplicada',
    'Tecnologias da Informação e Programação',
    'Robótica, Automação e Eletrônica',
    'Engenharia e Energias Renováveis',
    'Geociências e Sustentabilidade Ambiental',

    # Ciências Sociais Aplicadas e Ciências Humanas
    'História, Filosoa e Sociologia',
    'Geografia e Estudos Regionais',
    'Educação, Cidadania e Direitos Humanos',
    'Gestão, Empreendedorismo e Economia',
    'Comunicação, Informação e Cultura Digital',

    # Linguística, Letras e Artes
    'Língua Portuguesa e Produção Textual',
    'Línguas Estrangeiras e Multilinguismo',
    'Literatura, Leitura e Narrativas',
    'Artes Visuais, Dança e Teatro',
    'Música, Cinema e Audiovisual'
}

def import_works_from_csv(file_stream):
    """
    Importa trabalhos de um arquivo CSV
    Formato esperado: Nº,Orientador,Autores,Título,Área - Subárea,Tipo
    (Campo Nº é opcional e será ignorado)
    """
    try:
        df = pd.read_csv(
            file_stream,
            encoding='utf-8',
            quotechar='"',
            escapechar='\\',
            on_bad_lines='skip',
            skipinitialspace=True,
            engine='python',
            sep=',',
            header=0
        )

        return process_works_dataframe(df)

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            'success': False,
            'message': f'Erro ao processar arquivo CSV: {str(e)}',
            'errors': [str(e), f'Detalhes: {error_details}'],
            'imported_count': 0
        }

def process_works_dataframe(df):
    """
    Processa um DataFrame do pandas (CSV)
    """
    try:

        # debug
        print(f"Colunas detectadas: {list(df.columns)}")
        print(f"Número de colunas: {len(df.columns)}")

        required_columns = ['Orientador', 'Autores', 'Título', 'Área - Subárea', 'Tipo']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Colunas obrigatórias não encontradas: {missing_columns}")

        column_mapping = {
            'orientador': 'Orientador',
            'autores': 'Autores',
            'titulo': 'Título',
            'area_subarea': 'Área - Subárea',
            'tipo': 'Tipo'
        }

        works = []
        errors = []

        for line_idx, (index, row) in enumerate(df.iterrows(), start=2):
            line_number = line_idx
            try:
                title = str(row.get(column_mapping['titulo'], '')).strip()
                authors = str(row.get(column_mapping['autores'], '')).strip()
                advisor = str(row.get(column_mapping['orientador'], '')).strip()
                work_type = str(row.get(column_mapping['tipo'], '')).strip().lower()

                area_subarea_value = str(row.get(column_mapping['area_subarea'], '')).strip()

                if ' - ' in area_subarea_value:
                    area_parts = area_subarea_value.split(' - ', 1)
                    area = area_parts[0].strip()
                    subarea = area_parts[1].strip()
                else:
                    if area_subarea_value in VALID_AREAS:
                        area = area_subarea_value
                        subarea = ''
                    else:
                        area = ''
                        subarea = area_subarea_value

                # Validar campos obrigatórios (incluindo NaN do pandas)
                if not title or title == 'nan' or title == 'None' or pd.isna(row.get(column_mapping['titulo'])):
                    errors.append(f"Linha {line_number}: Título é obrigatório")
                    continue

                if not authors or authors == 'nan' or authors == 'None' or pd.isna(row.get(column_mapping['autores'])):
                    errors.append(f"Linha {line_number}: Autores são obrigatórios")
                    continue

                if not advisor or advisor == 'nan' or advisor == 'None' or pd.isna(row.get(column_mapping['orientador'])):
                    errors.append(f"Linha {line_number}: Orientador é obrigatório")
                    continue

                # Validar área e subárea
                if not area:
                    errors.append(f"Linha {line_number}: Área é obrigatória (valor da coluna: '{area_subarea_value}')")
                    continue

                if area not in VALID_AREAS:
                    errors.append(f"Linha {line_number}: Área '{area}' não reconhecida")
                    continue

                if subarea not in VALID_SUBAREAS:
                    errors.append(f"Linha {line_number}: Subárea '{subarea}' não reconhecida")
                    continue

                if work_type not in ['pôster/banner', 'apresentação oral', 'poster_banner', 'oral_presentation']:
                    errors.append(f"Linha {line_number}: Tipo '{work_type}' não reconhecido. Use 'Pôster/Banner' ou 'Apresentação Oral'")
                    continue

                if work_type in ['pôster/banner', 'poster_banner']:
                    work_type = 'poster_banner'
                elif work_type in ['apresentação oral', 'oral_presentation']:
                    work_type = 'oral_presentation'

                work = Work(
                    title=title,
                    authors=authors,
                    advisor=advisor,
                    type=work_type,
                    area=area,
                    subarea=subarea
                )

                works.append(work)

            except Exception as e:
                errors.append(f"Linha {line_number}: Erro ao processar linha - {str(e)}")
                continue

        if not errors:
            for work in works:
                db.session.add(work)
            db.session.commit()
            return {
                'success': True,
                'message': f'{len(works)} trabalhos importados com sucesso!',
                'imported_count': len(works)
            }
        else:
            return {
                'success': False,
                'message': f'Erros encontrados durante a importação:',
                'errors': errors,
                'imported_count': 0
            }

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            'success': False,
            'message': f'Erro ao processar arquivo CSV: {str(e)}',
            'errors': [str(e), f'Detalhes: {error_details}'],
            'imported_count': 0
        }
