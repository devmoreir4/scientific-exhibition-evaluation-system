from app.models import Work, Evaluator, work_evaluator_association, db
import random

def distribute_works():
    works = Work.query.all()

    if not works:
        raise Exception('Não há trabalhos cadastrados para distribuir.')

    # Considers 'Pedagógica' as pedagogical evaluator, the rest as technical
    pedagogical_evaluators = Evaluator.query.filter(Evaluator.area.ilike('%pedag%')).all()
    technical_evaluators = Evaluator.query.filter(~Evaluator.area.ilike('%pedag%')).all()

    if not pedagogical_evaluators:
        raise Exception('É necessário pelo menos um avaliador pedagógico cadastrado.')

    if not technical_evaluators:
        raise Exception('É necessário pelo menos um avaliador técnico cadastrado.')

    # Check if there are enough evaluators for all subareas
    subareas = set(work.subarea for work in works)
    problematic_subareas = []

    for subarea in subareas:
        # Check available pedagogical evaluators for this subarea
        available_pedagogical_evaluators = 0
        for ped in pedagogical_evaluators:
            # Check if evaluator doesn't have works in this subarea
            advisor_works = Work.query.filter_by(advisor=ped.name).all()
            has_conflict = any(w.subarea == subarea for w in advisor_works)
            if not has_conflict:
                available_pedagogical_evaluators += 1

        # Check available technical evaluators for this subarea
        available_technical_evaluators = 0
        for tec in technical_evaluators:
            # Check if evaluator doesn't have works in this subarea AND has expertise in the area
            advisor_works = Work.query.filter_by(advisor=tec.name).all()
            has_conflict = any(w.subarea == subarea for w in advisor_works)

            # Check if evaluator has expertise in the work area
            work_example = next((w for w in works if w.subarea == subarea), None)
            has_expertise = False
            if work_example and tec.area == work_example.area:
                has_expertise = True

            if not has_conflict and has_expertise:
                available_technical_evaluators += 1

        if available_pedagogical_evaluators == 0:
            problematic_subareas.append(f'Subárea "{subarea}": Sem avaliadores pedagógicos disponíveis')
        elif available_technical_evaluators == 0:
            problematic_subareas.append(f'Subárea "{subarea}": Sem avaliadores técnicos disponíveis')

    if problematic_subareas:
        error_msg = 'Problemas encontrados na distribuição:\n' + '\n'.join(problematic_subareas)
        raise Exception(error_msg)

    # Clear previous associations
    db.session.execute(work_evaluator_association.delete())
    db.session.commit()

    # Reset workload
    for ev in pedagogical_evaluators + technical_evaluators:
        ev.workload = 0
    db.session.commit()

    for work in works:
        def can_evaluate(evaluator, work):
            if evaluator.name == work.advisor:
                return False

            advisor_works = Work.query.filter_by(advisor=evaluator.name).all()
            for advisor_work in advisor_works:
                if advisor_work.subarea == work.subarea:
                    return False

            return True

        def has_expertise(evaluator, work):
            if evaluator.area == work.area:
                return True
            return False

        eligible_pedagogical_evaluators = [p for p in pedagogical_evaluators if can_evaluate(p, work)]

        if not eligible_pedagogical_evaluators:
            raise Exception(f'Não há avaliadores pedagógicos disponíveis para o trabalho "{work.title}" (subárea: {work.subarea}).')

        # 1 pedagogical evaluator (least overloaded among eligible)
        ped = min(eligible_pedagogical_evaluators, key=lambda e: e.workload)
        work.evaluators.append(ped)
        ped.workload += 1

        # Filter eligible technical evaluators (with expertise in the area)
        eligible_technical_evaluators = [t for t in technical_evaluators if can_evaluate(t, work) and has_expertise(t, work)]

        if not eligible_technical_evaluators:
            raise Exception(f'Não há avaliadores técnicos com expertise na área "{work.area}" disponíveis para o trabalho "{work.title}" (subárea: {work.subarea}).')

        # 1 or 2 technical evaluators
        num_technical_evaluators = random.choice([1, 2])

        # Select technical evaluators with lowest workload
        eligible_technical_evaluators_sorted = sorted(eligible_technical_evaluators, key=lambda e: e.workload)
        min_workload = eligible_technical_evaluators_sorted[0].workload
        candidates = [t for t in eligible_technical_evaluators_sorted if t.workload == min_workload]
        random.shuffle(candidates)

        # Select the first num_technical_evaluators
        selected = candidates[:num_technical_evaluators]

        for t in selected:
            work.evaluators.append(t)
            t.workload += 1

    db.session.commit()
    return True
