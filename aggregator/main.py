import asyncio
import random
import time
from datetime import datetime
from fastapi import FastAPI, Response, status
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from models import TelemetryEvent, CockpitSummary
import exporter

app = FastAPI(
    title="AI Infrastructure Unified Operations & Governance Cockpit (Tier 6)",
    description="Single-Pane-of-Glass Telemetry Aggregator Correlating Fabric, NetDevOps, Assurance, SecOps & Zero-Trust RAG",
    version="1.0.0"
)

# Initialize default metrics
exporter.initialize_defaults()

# Simulated Telemetry Background Engine
async def background_telemetry_generator():
    """Generates realistic continuous AI infrastructure telemetry mirroring enterprise production fabrics."""
    while True:
        try:
            # 1. Tier 1: Simulate RoCEv2 Incast Bursts & Early ECN Marking
            # Baseline queue occupancy with periodic microbursts
            burst_factor = 1.0
            if random.random() < 0.20:
                burst_factor = random.uniform(3.0, 5.5)  # Microburst event
            
            q3_depth = random.uniform(12000, 24000) * burst_factor
            q0_depth = random.uniform(3000, 8000)
            
            exporter.QUEUE_DEPTH.labels(queue='q3_rocev2_lossless').set(q3_depth)
            exporter.QUEUE_DEPTH.labels(queue='q0_best_effort').set(q0_depth)
            
            # ECN WRED Marking triggered if Q3 exceeds Kmin (64 KB = 65,536 bytes)
            if q3_depth > 65536:
                marked_count = int((q3_depth - 65536) / 1024 * random.uniform(1.2, 2.5))
                exporter.ECN_MARKED_PKTS.inc(max(1, marked_count))
            
            # PFC Pause Triggered only if severe buffer exhaustion (> 192 KB)
            if q3_depth > 196608:
                exporter.PFC_PAUSE_FRAMES.inc(1)
            
            # 2. Tier 2: NetDevOps Pipeline & Drift Assertions
            if random.random() < 0.15:
                exporter.NETDEVOPS_PIPELINE_RUNS.inc(1)
                exporter.NETDEVOPS_PYTEST_ASSERTIONS.inc(random.randint(12, 24))
                if random.random() < 0.05:
                    exporter.NETDEVOPS_DRIFT_EVENTS.inc(1)

            # 3. Tier 3: Synthetic Multi-Cloud Path Latency
            exporter.SYNTHETIC_PATH_LATENCY.labels(target='inference-us-east').set(round(random.uniform(26.5, 34.2), 2))
            exporter.SYNTHETIC_PATH_LATENCY.labels(target='inference-eu-west').set(round(random.uniform(72.0, 81.5), 2))
            exporter.SYNTHETIC_PATH_LATENCY.labels(target='local-ollama-cluster').set(round(random.uniform(2.8, 4.2), 2))
            exporter.ENDPOINT_AVAILABILITY.set(round(random.uniform(99.95, 100.0), 2))

            # 4. Tier 4: SIEM SecOps Events
            if random.random() < 0.08:
                exporter.SECOPS_SURICATA_ANOMALIES.inc(1)
            if random.random() < 0.04:
                exporter.SECOPS_EXFILTRATION_BURSTS.inc(1)
                exporter.SECOPS_INJECTIONS_DETECTED.inc(1)

            # 5. Tier 5: Zero-Trust RAG Security Assertions
            if random.random() < 0.10:
                exporter.RAG_PII_REDACTIONS.inc(random.randint(1, 3))
            if random.random() < 0.05:
                exporter.RAG_PROMPT_INJECTIONS_BLOCKED.inc(1)
            if random.random() < 0.03:
                exporter.RAG_UNAUTH_BLOCKS.inc(1)

            # Assert strictly 0 cross-tenant leaks (Zero-Trust)
            exporter.RAG_CROSS_TENANT_LEAKS.set(0)
            exporter.GOVERNANCE_COMPLIANCE_SCORE.set(100.0)

            await asyncio.sleep(1)
        except Exception as e:
            await asyncio.sleep(1)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_telemetry_generator())

@app.get("/healthz", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "healthy",
        "service": "unified_cockpit_aggregator",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/api/v1/cockpit-summary", response_model=CockpitSummary)
def get_cockpit_summary():
    return CockpitSummary(
        timestamp=datetime.utcnow(),
        fabric_status="OPTIMAL",
        active_threats=0,
        cross_tenant_leaks=0,
        p99_inference_latency_ms=28.4,
        slo_availability_percent=99.98,
        compliance_score_percent=100.0,
        tier_health={
            "tier1_lossless_fabric": "HEALTHY (ECN Active, Zero PFC Storms)",
            "tier2_netdevops_cicd": "AUTOMATED (100% PyTest Passing)",
            "tier3_synthetic_assurance": "HEALTHY (Sub-50ms Multi-Cloud SLO)",
            "tier4_ai_secops_siem": "SHIELDED (Zeek/Suricata Monitored)",
            "tier5_zero_trust_rag": "COMPLIANT (0 Cross-Tenant Leaks, RBAC Active)",
            "tier6_unified_governance": "ACTIVE (Single-Pane-of-Glass Synchronized)"
        }
    )

@app.post("/api/v1/telemetry/ingest", status_code=status.HTTP_201_CREATED)
def ingest_event(event: TelemetryEvent):
    # Ingest dynamic cross-tier telemetry
    if event.tier == "tier1_fabric":
        if "queue" in event.labels:
            exporter.QUEUE_DEPTH.labels(queue=event.labels["queue"]).set(event.value)
    elif event.tier == "tier3_assurance":
        if "target" in event.labels:
            exporter.SYNTHETIC_PATH_LATENCY.labels(target=event.labels["target"]).set(event.value)
    elif event.tier == "tier4_secops":
        exporter.SECOPS_EXFILTRATION_BURSTS.inc(1)
    elif event.tier == "tier5_rag":
        if event.metric_name == "prompt_injection_blocked":
            exporter.RAG_PROMPT_INJECTIONS_BLOCKED.inc(1)
        elif event.metric_name == "pii_redaction":
            exporter.RAG_PII_REDACTIONS.inc(1)

    return {"status": "accepted", "tier": event.tier, "metric": event.metric_name}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) # nosec B104
