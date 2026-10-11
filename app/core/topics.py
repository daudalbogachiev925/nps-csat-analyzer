import numpy as np
from functools import lru_cache
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
from app.config import settings

@lru_cache(maxsize=1)
def _embedder():
    return SentenceTransformer(settings.EMBED_MODEL)

def extract_terms(texts, k=6):
    if not texts:
        return []
    vec = TfidfVectorizer(max_features=500, ngram_range=(1, 2), min_df=1)
    X = vec.fit_transform(texts)
    terms = vec.get_feature_names_out()
    scores = np.asarray(X.mean(axis=0)).ravel()
    top = scores.argsort()[::-1][:k]
    return [terms[i] for i in top]

def cluster_topics(feedbacks, n_topics=5):
    if len(feedbacks) < 3:
        return {}, {}
    vectors = _embedder().encode(feedbacks, normalize_embeddings=True)
    n = min(n_topics, len(feedbacks))
    km = KMeans(n_clusters=n, random_state=0, n_init=10).fit(vectors)
    labels = km.labels_

    summary = {}
    for cid in sorted(set(labels)):
        items = [f for f, c in zip(feedbacks, labels) if c == cid]
        summary[int(cid)] = {
            "size": len(items),
            "sample": items[0][:200] if items else "",
            "terms": extract_terms(items, k=6),
        }
    return {int(c): int(l) for c, l in zip(feedbacks, labels)}, summary
