from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from sqlalchemy.sql import func
from app.database import Base

class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    segment = Column(String, index=True)
    survey_type = Column(String, index=True)
    score = Column(Integer, nullable=False)
    feedback = Column(Text)
    topic_cluster = Column(Integer, index=True)
    sentiment = Column(String)
    created_at = Column(DateTime, server_default=func.now(), index=True)

    __table_args__ = (
        Index("ix_survey_segment", "survey_type", "segment"),
    )
