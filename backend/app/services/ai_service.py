import google.generativeai as genai
from PIL import Image
import json
import os
import io

def get_google_api_key():
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY não configurada.")
    return api_key

def get_ai_model():
    api_key = get_google_api_key()
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

PROMPT = """
Você é um assistente de IA especialista em extrair dados de formulários de avaliação científica.

IMPORTANTE: Analise APENAS a imagem fornecida. Se a imagem não for um formulário de avaliação válido, retorne null para todas as notas.

INSTRUÇÕES ESPECÍFICAS:
1. A imagem deve ser um formulário de avaliação com 5 questões
2. Cada questão deve ter opções de 1 a 5 (Ruim a Excelente)
3. Procure por marcas "X", checkboxes marcados, ou círculos preenchidos
4. Se não encontrar marcas claras, retorne null
5. Se a imagem não for um formulário válido, retorne null para todas as notas

VALIDAÇÕES:
- Se a imagem não contém um formulário de avaliação → retorne null para todas as notas
- Se não encontrar marcas claras → retorne null para todas as notas
- Se a imagem estiver vazia, borrada ou ilegível → retorne null para todas as notas
- Se não houver 5 questões → retorne null para todas as notas
- Se a imagem for uma foto aleatória, selfie, ou qualquer coisa que não seja um formulário → retorne null para todas as notas

EXEMPLOS DE IMAGENS INVÁLIDAS:
- Fotos de pessoas
- Selfies
- Imagens de paisagem
- Screenshots de redes sociais
- Qualquer imagem que não seja um formulário de avaliação

Formate a saída EXATAMENTE como um objeto JSON:
{
  "scores": [null, null, null, null, null]
}

Se não conseguir identificar nenhuma marca válida, retorne:
{
  "scores": [null, null, null, null, null]
}

NÃO INVENTE DADOS. Se não estiver certo, retorne null.
"""

def validate_scores(scores):
    if not isinstance(scores, list) or len(scores) != 5:
        return [None, None, None, None, None]

    validated_scores = []
    for score in scores:
        if score is None:
            validated_scores.append(None)
        elif isinstance(score, (int, float)) and 1 <= score <= 5:
            validated_scores.append(int(score))
        else:
            validated_scores.append(None)

    return validated_scores

def process_sheet_image_ai(image_bytes):

    img = Image.open(io.BytesIO(image_bytes))

    if img.size[0] < 100 or img.size[1] < 100:
        return {
            'extracted_scores': [None, None, None, None, None],
            'warning': 'Use uma imagem com resolução mínima de 100x100 pixels.'
        }

    try:
        model = get_ai_model()
        response = model.generate_content([PROMPT, img])

        json_response_text = response.text.strip().replace('```json', '').replace('```', '')

        dados_extraidos = json.loads(json_response_text)

        # Validar os scores extraídos
        scores = dados_extraidos.get('scores', [])
        validated_scores = validate_scores(scores)

        if all(score is None for score in validated_scores):
            return {
                'extracted_scores': validated_scores,
                'warning': 'Nenhuma marca válida encontrada.'
            }

        return {
            'extracted_scores': validated_scores
        }

    except json.JSONDecodeError as e:
        return {
            'extracted_scores': [None, None, None, None, None],
            'warning': 'Erro ao processar resposta da IA.'
        }
    except Exception as e:
        raise ValueError(f'Erro ao processar imagem com IA: {str(e)}')
