# import cv2
# import re
# import pytesseract
# import numpy as np
# from PIL import Image
# import io

# LIMIAR_PIXELS = 200
# TAMANHO_ROI = 30

# coordenadas_centros = [
#     (142, 750), (312, 750), (503, 748), (678, 750), (859, 748),
#     (140, 893), (312, 897), (505, 893), (678, 893), (858, 895),
#     (140, 1037), (312, 1037), (508, 1039), (678, 1039), (859, 1037),
#     (142, 1181), (313, 1185), (503, 1181), (678, 1181), (861, 1183),
#     (140, 1366), (313, 1365), (505, 1365), (676, 1366), (859, 1366)
# ]

# rotulos_questoes = [
#     "Qualidade visual do pôster",
#     "Estrutura do pôster (introdução, métodos, resultados, conclusões)",
#     "Relevância social, ambiental, cultural ou tecnológica",
#     "Criatividade e originalidade da proposta",
#     "Expressão oral (volume, clareza e pausa) e domínio do assunto (conceitos, linguagem e termos técnicos)"
# ]
# rotulos_opcoes = ["1-Ruim", "2-Regular", "3-Bom", "4-Ótimo", "5-Excelente"]

# def process_sheet_image(image_bytes):
#     image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
#     img = np.array(image)
#     img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

#     # extração dos campos de texto
#     texto_completo_para_ocr = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     texto_extraido = pytesseract.image_to_string(texto_completo_para_ocr, lang='por')
#     id_poster = re.search(r'ID do pôster/banner:\s*(\d+)', texto_extraido)
#     avaliador = re.search(r'Avaliador:\s*(.+)', texto_extraido)

#     extracted_work_id = id_poster.group(1).strip() if id_poster else "Não encontrado"
#     extracted_work_evaluator = avaliador.group(1).strip().split('\n')[0] if avaliador else "Não encontrado"

#     # análise checkboxes
#     cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     binaria = cv2.adaptiveThreshold(cinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

#     respostas = {}
#     extracted_scores = []
#     for i, (cx, cy) in enumerate(coordenadas_centros):
#         id_questao = i // 5
#         id_opcao = i % 5
#         meio_roi = TAMANHO_ROI // 2
#         y1, y2 = cy - meio_roi, cy + meio_roi
#         x1, x2 = cx - meio_roi, cx + meio_roi
#         roi = binaria[y1:y2, x1:x2]
#         pixels_marcados = cv2.countNonZero(roi)
#         nome_questao = rotulos_questoes[id_questao]

#         if nome_questao not in respostas:
#             respostas[nome_questao] = "Não marcado"

#         if pixels_marcados > LIMIAR_PIXELS:
#             respostas[nome_questao] = rotulos_opcoes[id_opcao]

#     for questao in rotulos_questoes:
#         valor = respostas.get(questao, "Não marcado")
#         if valor == "Não marcado":
#             extracted_scores.append(None)
#         else:
#             extracted_scores.append(int(valor.split('-')[0]))

#     return {
#         'extracted_work_id': extracted_work_id,
#         'extracted_work_evaluator': extracted_work_evaluator,
#         'extracted_scores': extracted_scores
#     }
