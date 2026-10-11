def test_health(client):
    assert client.get("/health").json()["status"] == "ok"

def test_add_response(client):
    r = client.post("/api/responses", json={
        "user_id": "u1", "segment": "smb", "survey_type": "nps",
        "score": 9, "feedback": "Great"})
    assert r.status_code == 201

def test_nps_endpoint(client):
    client.post("/api/responses", json={
        "user_id": "u1", "survey_type": "nps", "score": 10})
    client.post("/api/responses", json={
        "user_id": "u2", "survey_type": "nps", "score": 3})
    r = client.get("/api/analytics/nps")
    assert r.status_code == 200
    assert r.json()["total"] == 2

def test_nps_by_segment(client):
    client.post("/api/responses", json={
        "user_id": "u1", "segment": "smb", "survey_type": "nps", "score": 10})
    r = client.get("/api/analytics/nps/by-segment")
    assert r.status_code == 200
    assert "smb" in r.json()

def test_batch(client):
    r = client.post("/api/responses/batch", json=[
        {"user_id": "u2", "survey_type": "nps", "score": 9},
        {"user_id": "u3", "survey_type": "nps", "score": 3},
    ])
    assert r.json()["inserted"] == 2
