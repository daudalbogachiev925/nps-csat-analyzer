def compute_csat(responses):
    if not responses:
        return {"csat": 0.0, "satisfied": 0, "total": 0}
    satisfied = sum(1 for r in responses if r.score >= 4)
    return {"csat": round(satisfied / len(responses) * 100, 1),
            "satisfied": satisfied, "total": len(responses)}
