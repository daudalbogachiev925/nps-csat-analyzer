from app.core.csat import compute_csat

class R:
    def __init__(self, s): self.score = s

def test_csat():
    responses = [R(5), R(4), R(3), R(2), R(5)]
    r = compute_csat(responses)
    assert r["csat"] == 60.0
    assert r["satisfied"] == 3

def test_csat_empty():
    r = compute_csat([])
    assert r["csat"] == 0.0
