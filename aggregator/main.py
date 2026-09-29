import os
import glob
import json
from datetime import datetime
from fastapi import FastAPI, Response, status, HTTPException
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from models import EvidenceRecord, GovernancePosture, ControlFinding
from engine import ControlEvaluationEngine
import exporter

app = FastAPI(
    title="Unified AI Infrastructure Governance Control Plane (LAB 07)",
    description="Evidence & Control Plane Engine consuming signed evidence records from Labs 01-06 to derive explainable operational posture and compliance.",
    version="1.0.0"
)

# Instantiate the Control Evaluation Engine
engine = ControlEvaluationEngine()

@app.on_event("startup")
def startup_event():
    """Auto-loads existing evidence records from disk on startup if available."""
    evidence_dirs = [
        "/app/data/evidence",
        "poc/evidence",
        "data/evidence"
    ]
    for d in evidence_dirs:
        if os.path.exists(d):
            print(f"[*] Loading historical evidence records from {d}...")
            for fpath in glob.glob(f"{d}/*.json"):
                try:
                    with open(fpath, "r") as f:
                        data = json.load(f)
                        rec = EvidenceRecord(**data)
                        engine.ingest_evidence(rec)
                        print(f"  [+] Ingested baseline evidence from {fpath}: {rec.experiment.id}")
                except Exception as e:
                    print(f"[-] Evidence load error for {fpath}: {e}")

    exporter.update_prometheus_metrics(engine)

@app.get("/healthz", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "healthy",
        "service": "unified_governance_control_plane",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.get("/metrics")
def metrics():
    exporter.update_prometheus_metrics(engine)
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/api/v1/summary", response_model=GovernancePosture)
def get_governance_summary():
    """Returns the overall governance posture derived from real ingested evidence."""
    exporter.update_prometheus_metrics(engine)
    return engine.get_posture()

@app.get("/api/v1/controls", response_model=list[ControlFinding])
def list_controls():
    """Returns individual control evaluations with evidence provenance and freshness tracking."""
    exporter.update_prometheus_metrics(engine)
    return engine.evaluate_controls()

@app.post("/api/v1/evidence/ingest", status_code=status.HTTP_201_CREATED)
def ingest_evidence(evidence: EvidenceRecord):
    """Ingests a signed/validated evidence record emitted by a laboratory experiment."""
    res = engine.ingest_evidence(evidence)
    exporter.EVIDENCE_INGESTION_TOTAL.labels(source_lab=evidence.execution.environment).inc(1)
    exporter.update_prometheus_metrics(engine)
    return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)  # nosec B104
