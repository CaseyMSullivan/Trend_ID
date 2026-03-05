# Text Processing Module
from collections import Counter
import re
from typing import Dict

# Stopwords
STOPWORDS = set([
    'the','and','that','with','this','from','they','your','have','will','just',
    'but','also','more','into','when','what','for','their','not','you','can',
    'about','like','use','using','are','has','its','we','our','in','on','of','as','at','or'
])

def tokenize(text: str) -> list:
    # Tokenize text into lowercase alphabetic words length >= 4 and remove stopwords.
    text = text.lower()
    tokens = re.findall(r'\b[a-z]{4,}\b', text)
    return [t for t in tokens if t not in STOPWORDS]

def compute_trend_scores(docs: Dict[str, str]):
    # Compute term frequency, document frequency, recent/earlier splitting.
    term_freq = Counter()
    term_doc_count = Counter()
    doc_names = sorted(docs.keys())
    recent_docs = doc_names[-3:] if len(doc_names) >= 3 else doc_names
    earlier_docs = doc_names[:-3]
    recent_tokens = Counter()
    earlier_tokens = Counter()
    for name, text in docs.items():
        tokens = tokenize(text)
        term_freq.update(tokens)
        for t in set(tokens):
            term_doc_count[t] += 1
        if name in recent_docs:
            recent_tokens.update(tokens)
        if name in earlier_docs:
            earlier_tokens.update(tokens)
    return term_freq, term_doc_count, recent_tokens, earlier_tokens

def classify_trends(term_freq, term_doc_count, recent_tokens, earlier_tokens, total_docs: int):
    # Classify terms into high, medium, low and find fads.
    high = {}
    medium = {}
    low = {}
    fads = []
    if not term_freq:
        return high, medium, low, fads
    freq_list = sorted(term_freq.values())
    median_freq = freq_list[len(freq_list)//2]
    breadth_required = max(3, total_docs // 3)
    for term, freq in term_freq.items():
        breadth = term_doc_count.get(term, 0)
        recent = recent_tokens.get(term, 0)
        earlier = earlier_tokens.get(term, 0)
        momentum = recent - earlier
        if earlier == 0 and recent > 0 and breadth == 1:
            fads.append(term)
            continue
        if freq >= 2 * median_freq and breadth >= breadth_required and momentum >= 0:
            high[term] = (freq, breadth, momentum)
        elif freq >= median_freq or breadth >= 2:
            medium[term] = (freq, breadth, momentum)
        else:
            low[term] = (freq, breadth, momentum)
    return high, medium, low, fads
