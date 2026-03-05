# OpenAI Validation Module
import openai
import json

def validate_term(term: str) -> dict:
    # Classify a term using OpenAI into beauty_trend, generic, or fad.
    if not openai.api_key:
        return {'classification': 'generic', 'reason': 'No OpenAI key provided.'}
    prompt = f'''You are a beauty market analyst. Classify the term '{term}' into:
- 'beauty_trend': a real, stable beauty trend
- 'generic': broad/common word that is not a trend
- 'fad': short-lived, hype-driven, low staying power
Return only JSON with keys 'classification' and 'reason'.'''
    try:
        response = openai.ChatCompletion.create(model='gpt-4o-mini', messages=[{'role': 'user', 'content': prompt}])
        data = json.loads(response['choices'][0]['message']['content'])
        return data
    except Exception as e:
        return {'classification': 'generic', 'reason': str(e)}