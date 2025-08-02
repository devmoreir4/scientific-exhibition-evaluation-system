from app.models import Work, Evaluator, work_evaluator_association, db
import random

def distribute_works():
    works = Work.query.all()
    # Considera 'Pedagógica' como avaliador pedagógico, o resto como técnico
    pedagogicos = Evaluator.query.filter(Evaluator.area.ilike('%pedag%')).all()
    tecnicos = Evaluator.query.filter(~Evaluator.area.ilike('%pedag%')).all()

    if not pedagogicos or not tecnicos:
        raise Exception('É necessário pelo menos um avaliador pedagógico e um técnico.')

    # Verificar se há avaliadores suficientes para todas as subáreas
    subareas = set(work.subarea for work in works)
    problematic_subareas = []

    for subarea in subareas:
        # Verificar avaliadores pedagógicos disponíveis para esta subárea
        pedagogicos_disponiveis = 0
        for ped in pedagogicos:
            # Verificar se não tem trabalhos nesta subárea
            orientador_works = Work.query.filter_by(advisor=ped.name).all()
            tem_conflito = any(w.subarea == subarea for w in orientador_works)
            if not tem_conflito:
                pedagogicos_disponiveis += 1

        # Verificar avaliadores técnicos disponíveis para esta subárea
        tecnicos_disponiveis = 0
        for tec in tecnicos:
            # Verificar se não tem trabalhos nesta subárea E se tem expertise na área
            orientador_works = Work.query.filter_by(advisor=tec.name).all()
            tem_conflito = any(w.subarea == subarea for w in orientador_works)

            # Verificar se o avaliador tem expertise na área do trabalho
            # Buscar um trabalho desta subárea para verificar a área
            work_example = next((w for w in works if w.subarea == subarea), None)
            tem_expertise = False
            if work_example and tec.area == work_example.area:
                tem_expertise = True

            # Verificar se tem subárea de interesse (opcional, mas melhora a qualidade)
            tem_subarea_interesse = False
            if work_example and tec.area == work_example.area and tec.subareas and work_example.subarea in tec.subareas.split(';'):
                tem_subarea_interesse = True

            if not tem_conflito and tem_expertise:
                tecnicos_disponiveis += 1

        if pedagogicos_disponiveis == 0:
            problematic_subareas.append(f'Subárea "{subarea}": Sem avaliadores pedagógicos disponíveis')
        elif tecnicos_disponiveis == 0:
            problematic_subareas.append(f'Subárea "{subarea}": Sem avaliadores técnicos disponíveis')

    if problematic_subareas:
        error_msg = 'Problemas encontrados na distribuição:\n' + '\n'.join(problematic_subareas)
        raise Exception(error_msg)

    # Limpar associações anteriores
    db.session.execute(work_evaluator_association.delete())
    db.session.commit()

    # Resetar carga
    for ev in pedagogicos + tecnicos:
        ev.carga = 0
    db.session.commit()

    for work in works:
        # Verificar se avaliador pode avaliar este trabalho
        def can_evaluate(evaluator, work):
            if evaluator.name == work.advisor:
                return False

            orientador_works = Work.query.filter_by(advisor=evaluator.name).all()
            for orientador_work in orientador_works:
                if orientador_work.subarea == work.subarea:
                    return False

            return True

        # Verificar se avaliador tem expertise na área/subárea do trabalho
        def has_expertise(evaluator, work):
            if evaluator.area == work.area:
                return True

            return False

        # Verificar se avaliador tem subárea de interesse correspondente (prioridade)
        def has_subarea_interest(evaluator, work):
            if evaluator.area == work.area and evaluator.subareas and work.subarea in evaluator.subareas.split(';'):
                return True
            return False

        pedagogicos_elegiveis = [p for p in pedagogicos if can_evaluate(p, work)]

        if not pedagogicos_elegiveis:
            raise Exception(f'Não há avaliadores pedagógicos disponíveis para o trabalho "{work.title}" (subárea: {work.subarea}).')

        # 1 avaliador pedagógico (menos sobrecarregado entre os elegíveis)
        ped = min(pedagogicos_elegiveis, key=lambda e: e.carga)
        work.evaluators.append(ped)
        ped.carga += 1

        # Filtrar avaliadores técnicos elegíveis (com expertise na área)
        tecnicos_elegiveis = [t for t in tecnicos if can_evaluate(t, work) and has_expertise(t, work)]

        if not tecnicos_elegiveis:
            raise Exception(f'Não há avaliadores técnicos com expertise na área "{work.area}" disponíveis para o trabalho "{work.title}" (subárea: {work.subarea}).')

        # Separar avaliadores por prioridade (com e sem subárea de interesse)
        tecnicos_com_subarea = [t for t in tecnicos_elegiveis if has_subarea_interest(t, work)]
        tecnicos_sem_subarea = [t for t in tecnicos_elegiveis if not has_subarea_interest(t, work)]

        # 1 ou 2 técnicos (priorizando os com subárea de interesse)
        n_tecnicos = random.choice([1, 2])
        selecionados = []

        # Primeiro, tentar selecionar dos que têm subárea de interesse
        if tecnicos_com_subarea:
            tecnicos_com_subarea_sorted = sorted(tecnicos_com_subarea, key=lambda e: e.carga)
            min_carga = tecnicos_com_subarea_sorted[0].carga
            candidatos_com_subarea = [t for t in tecnicos_com_subarea_sorted if t.carga == min_carga]
            random.shuffle(candidatos_com_subarea)
            selecionados.extend(candidatos_com_subarea[:n_tecnicos])

        # Se ainda precisa de mais avaliadores, pegar dos que não têm subárea de interesse
        if len(selecionados) < n_tecnicos and tecnicos_sem_subarea:
            tecnicos_sem_subarea_sorted = sorted(tecnicos_sem_subarea, key=lambda e: e.carga)
            min_carga = tecnicos_sem_subarea_sorted[0].carga
            candidatos_sem_subarea = [t for t in tecnicos_sem_subarea_sorted if t.carga == min_carga]
            random.shuffle(candidatos_sem_subarea)
            selecionados.extend(candidatos_sem_subarea[:n_tecnicos - len(selecionados)])

        # Se ainda não tem avaliadores suficientes, pegar qualquer um elegível
        if len(selecionados) < n_tecnicos:
            todos_elegiveis = tecnicos_com_subarea + tecnicos_sem_subarea
            todos_elegiveis_sorted = sorted(todos_elegiveis, key=lambda e: e.carga)
            min_carga = todos_elegiveis_sorted[0].carga
            candidatos_todos = [t for t in todos_elegiveis_sorted if t.carga == min_carga]
            random.shuffle(candidatos_todos)
            # Remover duplicatas
            ids_selecionados = [s.id for s in selecionados]
            candidatos_nao_selecionados = [t for t in candidatos_todos if t.id not in ids_selecionados]
            selecionados.extend(candidatos_nao_selecionados[:n_tecnicos - len(selecionados)])

        for t in selecionados:
            work.evaluators.append(t)
            t.carga += 1

    db.session.commit()
    return True
