import google.generativeai as genai
from PIL import Image
import json
import os
import io

def process_sheet_image_ai(image_bytes):
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY não configurada")
    
    genai.configure(api_key=GOOGLE_API_KEY)
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    img = Image.open(io.BytesIO(image_bytes))
    
    prompt = """
    Você é um assistente de IA especialista em extrair dados de formulários de avaliação.
    Analise a imagem da ficha de avaliação preenchida e extraia as seguintes informações:

    1.  **ID do Pôster/Banner:** O número que está no campo "ID do pôster/banner" (retorne como string).
    2.  **Nome do Avaliador:** O nome que está no campo "Avaliador".
    3.  **Notas das Questões:** Para cada uma das 5 questões, identifique a opção marcada com "X" e retorne apenas o número da nota (de 1 a 5). Se uma questão não estiver marcada, retorne null.

    Formate a saída final EXATAMENTE como um objeto JSON, usando as seguintes chaves:
    - "work_id" (string - para o ID do pôster)
    - "evaluator_name" (string - para o nome do avaliador)
    - "scores" (array - uma lista com as 5 notas numéricas)

    Não inclua nenhuma outra explicação ou texto na sua resposta, apenas o JSON.
    """
    
    try:
        response = model.generate_content([prompt, img])
        
        json_response_text = response.text.strip().replace('```json', '').replace('```', '')
        
        dados_extraidos = json.loads(json_response_text)
        
        return {
            'extracted_work_id': str(dados_extraidos.get('work_id', 'Não encontrado')),
            'extracted_work_evaluator': dados_extraidos.get('evaluator_name', 'Não encontrado'),
            'extracted_scores': dados_extraidos.get('scores', [])
        }
        
    except json.JSONDecodeError as e:
        raise ValueError(f'Erro ao decodificar JSON da resposta da IA: {str(e)}')
    except Exception as e:
        raise ValueError(f'Erro ao processar imagem com IA: {str(e)}')