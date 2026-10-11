from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Response
from app.schemas import NpsScore, CsatScore, TopicSummary
from app.core.nps import compute_nps, classify
from app.core.csat import compute_csat
from app.core.topics import cluster_topics

router = APIRouter()

@router.get("/nps", response_model=NpsScore)
def nps(segment: str = None, db: Session = Depends(get_db)):
    q = db.query(Response).filter(Response.survey_type == "nps")
    if segment:
        q = q.filter(Response.segment == segment)
    return compute_nps(q.all())

@router.get("/nps/by-segment")
def nps_by_segment(db: Session = Depends(get_db)):
    rows = db.query(Response).filter(Response.survey_type == "nps").all()
    segments = {}
    for r in rows:
        segments.setdefault(r.segment or "unknown", []).append(r)
    return {seg: compute_nps(items) for seg, items in segments.items()}

@router.get("/csat", response_model=CsatScore)
def csat(db: Session = Depends(get_db)):
    rows = db.query(Response).filter(Response.survey_type == "csat").all()
    return compute_csat(rows)

@router.post("/topics", response_model=List[TopicSummary])
def topics(db: Session = Depends(get_db), only_detractors: bool = False):
    rows = db.query(Response).all()
    if only_detractors:
        rows = [r for r in rows if classify(r.score) == "detractor"]

    feedbacks = [r.feedback for r in rows if r.feedback]
    if not feedbacks:
        return []

    labels, summary = cluster_topics(feedbacks)

    for r in rows:
        if r.feedback in labels:
            r.topic_cluster = labels[r.feedback]
    db.commit()

    result = []
    for cid, info in summary.items():
        cluster_rows = [r for r in rows if r.topic_cluster == cid]
        avg_score = sum(r.score for r in cluster_rows) / max(len(cluster_rows), 1)
        result.append(TopicSummary(cluster_id=cid, size=info["size"],
                                    sample=info["sample"],
                                    sample_terms=info["terms"],
                                    avg_score=round(avg_score, 1)))
    return result

@router.get("/distribution")
def distribution(db: Session = Depends(get_db), survey_type: str = "nps"):
    rows = db.query(Response).filter(Response.survey_type == survey_type).all()
    dist = {}
    for r in rows:
        dist[r.score] = dist.get(r.score, 0) + 1
    return {"distribution": dist, "total": len(rows)}
