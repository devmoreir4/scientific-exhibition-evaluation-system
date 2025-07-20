from app.models import Work, Evaluator, work_evaluator_association, db
import random

def distribute_works():
    works = Work.query.all()
    # Considera 'Pedagógica' como avaliador pedagógico, o resto como técnico
    pedagogicos = Evaluator.query.filter(Evaluator.area.ilike('%pedag%')).all()
    tecnicos = Evaluator.query.filter(~Evaluator.area.ilike('%pedag%')).all()

    if not pedagogicos or not tecnicos:
        raise Exception('É necessário pelo menos um avaliador pedagógico e um técnico.')

    # Limpar associações anteriores
    db.session.execute(work_evaluator_association.delete())
    db.session.commit()

    # Resetar carga
    for ev in pedagogicos + tecnicos:
        ev.carga = 0
    db.session.commit()

    for work in works:
        # 1 avaliador pedagógico (menos sobrecarregado)
        ped = min(pedagogicos, key=lambda e: e.carga)
        work.evaluators.append(ped)
        ped.carga += 1

        # 1 ou 2 técnicos (menos sobrecarregados, randomizando em caso de empate)
        n_tecnicos = random.choice([1, 2])
        tecnicos_sorted = sorted(tecnicos, key=lambda e: e.carga)
        min_carga = tecnicos_sorted[0].carga
        candidatos = [t for t in tecnicos_sorted if t.carga == min_carga]
        random.shuffle(candidatos)
        selecionados = candidatos[:n_tecnicos]
        for t in selecionados:
            work.evaluators.append(t)
            t.carga += 1

    db.session.commit()
    return True 