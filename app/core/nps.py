def classify(score):
    if score >= 9: return "promoter"
    if score >= 7: return "passive"
    return "detractor"

def compute_nps(responses):
    counts = {"promoter": 0, "passive": 0, "detractor": 0}
    for r in responses:
        counts[classify(r.score)] += 1
    total = sum(counts.values())
    if total == 0:
        return {"nps": 0.0, "promoters": 0, "passives": 0,
                "detractors": 0, "total": 0}
    nps = (counts["promoter"] - counts["detractor"]) / total * 100
    return {"nps": round(nps, 1), "promoters": counts["promoter"],
            "passives": counts["passive"], "detractors": counts["detractor"],
            "total": total}
