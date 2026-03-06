import openai
import json

# Classifying each term using OpenAI.
def validate_term(term: str) -> dict:
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
