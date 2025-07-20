# import pandas as pd
# from app.models import Work
# from app.extensions import db

# def import_works_from_csv(file_stream):
#     df = pd.read_csv(file_stream)
#     works = []
#     for _, row in df.iterrows():
#         work = Work(
#             title=row['Título do trabalho'],
#             author=row['Autor/ Curso/ Instituição'],
#             area=row['Área'],
#             subarea=row['Subárea'],
#             abstract=row['Resumo'],
#             has_technical_student=True if str(row['Indicador se há aluno do curso técnico envolvido']).strip().lower() == 'sim' else False,
#             has_prototype=True if str(row['Indicador se o trabalho apresenta protótipo ou produto']).strip().lower() == 'sim' else False
#         )
#         db.session.add(work)
#         works.append(work)
#     db.session.commit()
#     return works 