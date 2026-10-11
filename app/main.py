from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.api import responses, analytics

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NPS CSAT Analyzer", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])
app.include_router(responses.router, prefix="/api/responses", tags=["responses"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "nps-csat-analyzer"}
