from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class ResponseCreate(BaseModel):
    user_id: str
    segment: Optional[str] = None
    survey_type: str = Field(pattern="^(nps|csat)$")
    score: int = Field(ge=0, le=10)
    feedback: Optional[str] = None

class ResponseRead(ResponseCreate):
    id: int
    topic_cluster: Optional[int]
    sentiment: Optional[str]
    created_at: Optional[datetime]
    class Config:
        from_attributes = True

class NpsScore(BaseModel):
    nps: float
    promoters: int
    passives: int
    detractors: int
    total: int

class CsatScore(BaseModel):
    csat: float
    satisfied: int
    total: int

class TopicSummary(BaseModel):
    cluster_id: int
    size: int
    sample: str
    sample_terms: List[str]
    avg_score: float
