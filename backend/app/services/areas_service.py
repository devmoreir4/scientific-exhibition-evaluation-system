AREAS_SUBAREAS = {
    'Pedagógica': [],  # Can evaluate any subarea

    'Ciências Agrárias': [
        'Agricultura e Sustentabilidade no Campo',
        'Zootecnia e Produção Animal',
        'Agroindústria e Alimentos',
        'Recursos Naturais e Meio Ambiente Rural',
        'Tecnologias e Processos Agrícolas'
    ],

    'Ciências Biológicas e Ciências da Saúde': [
        'Biotecnologia e Microbiologia',
        'Ecologia e Conservação',
        'Saúde Coletiva e Educação em Saúde',
        'Nutrição, Enfermagem e Bem-estar',
        'Práticas Integrativas e Promoção da Saúde'
    ],

    'Ciências Exatas e da Terra e Engenharias': [
        'Matemática, Física e Química Aplicada',
        'Tecnologias da Informação e Programação',
        'Robótica, Automação e Eletrônica',
        'Engenharia e Energias Renováveis',
        'Geociências e Sustentabilidade Ambiental'
    ],

    'Ciências Sociais Aplicadas e Ciências Humanas': [
        'História, Filosofia e Sociologia',
        'Geografia e Estudos Regionais',
        'Educação, Cidadania e Direitos Humanos',
        'Gestão, Empreendedorismo e Economia',
        'Comunicação, Informação e Cultura Digital'
    ],

    'Linguística, Letras e Artes': [
        'Língua Portuguesa e Produção Textual',
        'Línguas Estrangeiras e Multilinguismo',
        'Literatura, Leitura e Narrativas',
        'Artes Visuais, Dança e Teatro',
        'Música, Cinema e Audiovisual'
    ]
}

def get_all_areas():
    return list(AREAS_SUBAREAS.keys())

def get_subareas_by_area(area):
    return AREAS_SUBAREAS.get(area, [])

def get_all_subareas():
    all_subareas = []
    for area, subareas in AREAS_SUBAREAS.items():
        if area != 'Pedagógica':
            all_subareas.extend(subareas)
    return all_subareas

def validate_area_subarea(area, subareas_list):
    if area == 'Pedagógica':
        valid_subareas = get_all_subareas()
    else:
        valid_subareas = get_subareas_by_area(area)

    if not valid_subareas and area != 'Pedagógica':
        return False, f"Área '{area}' não encontrada"

    for subarea in subareas_list:
        if subarea not in valid_subareas:
            return False, f"Subárea '{subarea}' não é válida para a área '{area}'"

    return True, "Válido"

def get_areas_summary():
    summary = {}
    for area, subareas in AREAS_SUBAREAS.items():
        if area == 'Pedagógica':
            summary[area] = {
                'subareas_count': len(get_all_subareas()),
                'description': 'Pode avaliar qualquer subárea'
            }
        else:
            summary[area] = {
                'subareas_count': len(subareas),
                'description': f'{len(subareas)} subáreas específicas'
            }
    return summary

def is_area_valid(area):
    return area in AREAS_SUBAREAS

def is_subarea_valid_for_area(area, subarea):
    if area == 'Pedagógica':
        return subarea in get_all_subareas()
    else:
        return subarea in get_subareas_by_area(area)
