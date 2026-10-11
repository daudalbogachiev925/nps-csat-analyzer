from app.core.topics import extract_terms

def test_extract_terms():
    feedbacks = ["slow app crash", "slow crash again", "fast simple design"]
    terms = extract_terms(feedbacks, k=3)
    assert len(terms) == 3

def test_extract_empty():
    assert extract_terms([], k=3) == []
