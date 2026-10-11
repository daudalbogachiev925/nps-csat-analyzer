from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Response
from app.schemas import ResponseCreate, ResponseRead

router = APIRouter()

@router.post("", response_model=ResponseRead, status_code=201)
def add(payload: ResponseCreate, db: Session = Depends(get_db)):
    r = Response(**payload.model_dump())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

@router.post("/batch", status_code=201)
def add_batch(payloads: List[ResponseCreate], db: Session = Depends(get_db)):
    for p in payloads:
        db.add(Response(**p.model_dump()))
    db.commit()
    return {"inserted": len(payloads)}

@router.get("", response_model=List[ResponseRead])
def list_all(survey_type: str = None, segment: str = None,
             db: Session = Depends(get_db), limit: int = 1000):
    q = db.query(Response)
    if survey_type:
        q = q.filter(Response.survey_type == survey_type)
    if segment:
        q = q.filter(Response.segment == segment)
    return q.limit(limit).all()

@router.delete("", status_code=204)
def delete_all(db: Session = Depends(get_db)):
    db.query(Response).delete()
    db.commit()
