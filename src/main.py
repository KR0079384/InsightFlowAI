import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from src.config import settings
from src.data_engine.loader import loader
from src.data_engine.simulator import simulator_engine
from src.decision_engine.engine import decision_engine
from src.decision_engine.evidence import evidence_engine
from src.models.schemas import (
    QueryRequest,
    DecisionReport,
    SimulationRequest,
    SimulationResponse,
    DatasetOverview,
    EvidenceItem
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="TraceIQ — AI Decision Engine for Business Data API",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "TraceIQ Decision Engine",
        "version": "1.0.0",
        "core_principle": "LLM proposes. Data engine proves."
    }

@app.get("/api/v1/overview", response_model=DatasetOverview)
def get_dataset_overview():
    return loader.get_overview()

@app.post("/api/v1/analyze", response_model=DecisionReport)
def analyze_business_question(payload: QueryRequest):
    if not payload.question or len(payload.question.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    return decision_engine.analyze_query(payload.question)

@app.post("/api/v1/simulate", response_model=SimulationResponse)
def simulate_scenario(payload: SimulationRequest):
    return simulator_engine.run_simulation(payload)

@app.get("/api/v1/evidence/{evidence_id}", response_model=EvidenceItem)
def get_evidence_detail(evidence_id: str):
    all_evs = evidence_engine.get_all_evidences()
    for ev in all_evs:
        if ev.id == evidence_id or evidence_id in ev.id:
            return ev
    # If specific match not found, return revenue decline default evidence
    if all_evs:
        return all_evs[0]
    raise HTTPException(status_code=404, detail="Evidence not found")

@app.get("/api/v1/products")
def list_products():
    if loader.products.empty:
        return []
    return loader.products.to_dict(orient="records")

# Mount built frontend dist if available
frontend_dist_path = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if frontend_dist_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist_path), html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("src.main:app", host=settings.HOST, port=settings.PORT, reload=True)
