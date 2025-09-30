from app.models import Evaluation, Work, Evaluator
from app.extensions import db


def calculate_evaluation_progress(page=1, per_page=20):
    works = Work.query.all()
    evaluations = Evaluation.query.all()

    total_works = len(works)
    total_evaluations = len(evaluations)

    works_with_evaluations = {}

    for work in works:
        work_evaluations = [e for e in evaluations if e.work_id == work.id]
        evaluated_evaluator_ids = {e.evaluator_id for e in work_evaluations}

        pending_evaluators = []
        for evaluator in work.evaluators:
            if evaluator.id not in evaluated_evaluator_ids:
                pending_evaluators.append({
                    'id': evaluator.id,
                    'name': evaluator.name,
                    'siape_or_cpf': evaluator.siape_or_cpf
                })

        progress_percentage = 0
        if work.evaluators:
            progress_percentage = round((len(work_evaluations) / len(work.evaluators)) * 100, 1)

        works_with_evaluations[work.id] = {
            'work_id': work.id,
            'work_title': work.title,
            'work_area': work.area,
            'work_subarea': work.subarea,
            'total_evaluators': len(work.evaluators),
            'completed_evaluations': len(work_evaluations),
            'pending_evaluations': len(work.evaluators) - len(work_evaluations),
            'progress_percentage': progress_percentage,
            'pending_evaluators': pending_evaluators
        }

    total_expected_evaluations = sum(len(work.evaluators) for work in works)
    overall_progress = 0
    if total_expected_evaluations > 0:
        overall_progress = round((total_evaluations / total_expected_evaluations) * 100, 1)

    # Pagination of works
    all_works_progress = list(works_with_evaluations.values())
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_works = all_works_progress[start_idx:end_idx]

    return {
        'overall_stats': {
            'total_works': total_works,
            'total_evaluations': total_evaluations,
            'total_expected_evaluations': total_expected_evaluations,
            'overall_progress': overall_progress
        },
        'works_progress': paginated_works,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'pages': (len(all_works_progress) + per_page - 1) // per_page,
            'total': len(all_works_progress),
            'has_prev': page > 1,
            'has_next': end_idx < len(all_works_progress),
            'prev_num': page - 1 if page > 1 else None,
            'next_num': page + 1 if end_idx < len(all_works_progress) else None
        }
    }


def calculate_work_average_score(work_evaluations):
    if not work_evaluations:
        return 0, 0

    total_score = 0
    for evaluation in work_evaluations:
        total_score += (
            evaluation.criterion1 + evaluation.criterion2 +
            evaluation.criterion3 + evaluation.criterion4 +
            evaluation.criterion5
        )

    average_score = total_score / (len(work_evaluations) * 5)
    return round(average_score, 2), total_score


def generate_works_podium():
    works = Work.query.all()
    evaluations = Evaluation.query.all()

    works_by_area = {}
    for work in works:
        if work.area not in works_by_area:
            works_by_area[work.area] = []
        works_by_area[work.area].append(work)

    podium_data = {}

    for area, area_works in works_by_area.items():
        works_with_scores = []

        for work in area_works:
            work_evaluations = [e for e in evaluations if e.work_id == work.id]

            if work_evaluations:
                average_score, total_score = calculate_work_average_score(work_evaluations)

                works_with_scores.append({
                    'work_id': work.id,
                    'work_title': work.title,
                    'work_authors': work.authors,
                    'work_advisor': work.advisor,
                    'work_type': work.type,
                    'work_subarea': work.subarea,
                    'evaluations_count': len(work_evaluations),
                    'average_score': average_score,
                    'total_score': total_score
                })

        works_with_scores.sort(key=lambda x: x['average_score'], reverse=True)
        top_3 = works_with_scores[:3]

        podium_data[area] = {
            'area_name': area,
            'total_works': len(area_works),
            'evaluated_works': len(works_with_scores),
            'podium': top_3
        }

    return podium_data


def validate_evaluation_data(data, evaluator_id, work_id):
    errors = []

    criteria = [data.get(f'criterion{i}') for i in range(1, 6)]

    if not work_id or not all(c is not None for c in criteria):
        errors.append('Dados obrigatórios faltando')
        return False, errors

    for idx, criterion in enumerate(criteria, 1):
        if not isinstance(criterion, int) or criterion < 1 or criterion > 5:
            errors.append(f'Critério {idx} deve ser um número inteiro de 1 (Ruim) a 5 (Excelente)')

    work = Work.query.get(work_id)
    if not work:
        errors.append('Trabalho não encontrado')
        return False, errors

    evaluator = Evaluator.query.get(evaluator_id)
    if not evaluator:
        errors.append('Avaliador não encontrado')
        return False, errors

    if work not in evaluator.works:
        errors.append('Você não está autorizado a avaliar este trabalho')
        return False, errors

    existing = Evaluation.query.filter_by(
        evaluator_id=evaluator_id,
        work_id=work_id
    ).first()

    if existing:
        errors.append('Você já avaliou este trabalho')
        return False, errors

    if errors:
        return False, errors

    return True, criteria


def create_evaluation(evaluator_id, work_id, criteria, method='online'):
    evaluation = Evaluation(
        criterion1=criteria[0],
        criterion2=criteria[1],
        criterion3=criteria[2],
        criterion4=criteria[3],
        criterion5=criteria[4],
        evaluator_id=evaluator_id,
        work_id=work_id,
        method=method
    )

    db.session.add(evaluation)
    db.session.commit()

    return evaluation


def validate_ai_evaluation_data(data):
    work_id = data.get('work_id')
    scores = data.get('scores')
    evaluator_id = data.get('evaluator_id')

    if not work_id or not evaluator_id or not scores or len(scores) != 5:
        return False, 'Dados obrigatórios faltando'

    evaluator = Evaluator.query.get(evaluator_id)
    if not evaluator:
        return False, 'Avaliador não encontrado'

    work = Work.query.get(work_id)
    if not work:
        return False, 'Trabalho não encontrado'

    works_with_evaluators = Work.query.filter(Work.evaluators.any()).count()
    if works_with_evaluators == 0:
        return False, 'Nenhum trabalho foi distribuído ainda'

    if evaluator not in work.evaluators:
        return False, 'Este avaliador não foi atribuído para avaliar este trabalho'

    existing_evaluation = Evaluation.query.filter_by(
        evaluator_id=evaluator_id,
        work_id=work_id
    ).first()

    if existing_evaluation:
        return False, 'Este avaliador já avaliou este trabalho'

    for i, score in enumerate(scores):
        if not isinstance(score, (int, float)) or score < 1 or score > 5:
            return False, f'Critério {i+1} deve ser um número entre 1 e 5'

    return True, None


def create_ai_evaluation(work_id, evaluator_id, scores):
    evaluation = Evaluation(
        criterion1=scores[0],
        criterion2=scores[1],
        criterion3=scores[2],
        criterion4=scores[3],
        criterion5=scores[4],
        method='ai_processed',
        evaluator_id=evaluator_id,
        work_id=work_id
    )

    db.session.add(evaluation)
    db.session.commit()

    return evaluation


def get_evaluator_evaluations(evaluator_id):
    evaluations = Evaluation.query.filter_by(evaluator_id=evaluator_id).all()
    result = []

    for evaluation in evaluations:
        work = Work.query.get(evaluation.work_id)
        result.append({
            'id': evaluation.id,
            'work_id': evaluation.work_id,
            'work_title': work.title if work else 'Trabalho não encontrado',
            'criterion1': evaluation.criterion1,
            'criterion2': evaluation.criterion2,
            'criterion3': evaluation.criterion3,
            'criterion4': evaluation.criterion4,
            'criterion5': evaluation.criterion5,
            'method': evaluation.method
        })

    return result


def get_work_evaluations(work_id):
    evaluations = Evaluation.query.filter_by(work_id=work_id).all()
    result = []

    for evaluation in evaluations:
        result.append({
            'id': evaluation.id,
            'evaluator_id': evaluation.evaluator_id,
            'criterion1': evaluation.criterion1,
            'criterion2': evaluation.criterion2,
            'criterion3': evaluation.criterion3,
            'criterion4': evaluation.criterion4,
            'criterion5': evaluation.criterion5,
            'method': evaluation.method
        })

    return result


def get_evaluation_statistics():
    total_evaluations = Evaluation.query.count()
    total_works = Work.query.count()
    total_evaluators = Evaluator.query.count()

    online_evaluations = Evaluation.query.filter_by(method='online').count()
    ai_processed_evaluations = Evaluation.query.filter_by(method='ai_processed').count()

    active_evaluators = db.session.query(Evaluation.evaluator_id).distinct().count()

    return {
        'total_evaluations': total_evaluations,
        'total_works': total_works,
        'total_evaluators': total_evaluators,
        'active_evaluators': active_evaluators,
        'online_evaluations': online_evaluations,
        'ai_processed_evaluations': ai_processed_evaluations,
        'completion_rate': round((active_evaluators / total_evaluators * 100), 1) if total_evaluators > 0 else 0
    }
