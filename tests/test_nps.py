from app.core.nps import classify, compute_nps

class R:
    def __init__(self, s): self.score = s

def test_classify():
    assert classify(10) == "promoter"
    assert classify(9) == "promoter"
    assert classify(7) == "passive"
    assert classify(6) == "detractor"

def test_nps_calculation():
    responses = [R(10), R(9), R(8), R(6), R(3)]
    r = compute_nps(responses)
    assert r["promoters"] == 2
    assert r["passives"] == 2
    assert r["detractors"] == 1
    assert r["nps"] == 20.0

def test_nps_all_promoters():
    responses = [R(10)] * 10
    r = compute_nps(responses)
    assert r["nps"] == 100.0

def test_nps_empty():
    assert compute_nps([])["nps"] == 0.0
