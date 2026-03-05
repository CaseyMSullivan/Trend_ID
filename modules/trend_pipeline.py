# Trend Pipeline
from typing import Dict
from modules.text_processing import compute_trend_scores, classify_trends
from modules.openai_validator import validate_term

def run_pipeline(docs: Dict[str, str]):
    # Compute and validate trends.
    term_freq, term_doc_count, recent, earlier = compute_trend_scores(docs)
    high, medium, low, fads = classify_trends(term_freq, term_doc_count, recent, earlier, total_docs=len(docs))
    validated = {'high': {}, 'medium': {}, 'low': {}, 'fads': fads}
    for cat, terms in [('high', high), ('medium', medium), ('low', low)]:
        for term, stats in terms.items():
            res = validate_term(term)
            if res.get('classification') == 'beauty_trend':
                validated[cat][term] = {'stats': stats, 'reason': res.get('reason', '')}
    return validated