from prometheus_client import Gauge, Counter
from engine import ControlEvaluationEngine

# ==============================================================================
# PROMETHEUS METRICS DRIVEN BY ACTUAL EVIDENCE EVALUATION
# ==============================================================================
OVERALL_GOVERNANCE_STATUS = Gauge('ai_governance_overall_status', '1 = PASS, 0 = DEGRADED/UNKNOWN, -1 = FAIL')
TOTAL_REGISTERED_CONTROLS = Gauge('ai_governance_total_controls_count', 'Total governance controls in catalog')
PASSING_CONTROLS_COUNT = Gauge('ai_governance_passing_controls_count', 'Controls with verified passing evidence')
FAILING_CONTROLS_COUNT = Gauge('ai_governance_failing_controls_count', 'Controls with failing evidence')
STALE_CONTROLS_COUNT = Gauge('ai_governance_stale_controls_count', 'Controls whose evidence exceeded freshness SLO')
UNKNOWN_CONTROLS_COUNT = Gauge('ai_governance_unknown_controls_count', 'Controls with zero evidence received')

# Per-Control Status Gauge (1 = PASS, 0 = UNKNOWN/STALE, -1 = FAIL)
CONTROL_STATUS = Gauge('ai_governance_control_status', 'Status of individual governance control', ['control_id', 'tier', 'source_lab'])
CONTROL_FRESHNESS = Gauge('ai_governance_control_freshness_seconds', 'Seconds since last evidence ingestion', ['control_id'])

EVIDENCE_INGESTION_TOTAL = Counter('ai_governance_evidence_ingestion_total', 'Total evidence envelopes ingested', ['source_lab'])

def update_prometheus_metrics(engine: ControlEvaluationEngine):
    """Refreshes Prometheus gauges directly from actual control evaluation findings."""
    posture = engine.get_posture()

    status_map = {"PASS": 1.0, "DEGRADED": 0.0, "UNKNOWN": 0.0, "STALE": 0.0, "FAIL": -1.0}
    OVERALL_GOVERNANCE_STATUS.set(status_map.get(posture.overall_status, 0.0))
    TOTAL_REGISTERED_CONTROLS.set(posture.total_controls)
    PASSING_CONTROLS_COUNT.set(posture.passing_controls)
    FAILING_CONTROLS_COUNT.set(posture.failing_controls)
    STALE_CONTROLS_COUNT.set(posture.stale_controls)
    UNKNOWN_CONTROLS_COUNT.set(posture.unknown_controls)

    for c in posture.controls:
        c_val = 1.0 if c.status == "PASS" else (-1.0 if c.status == "FAIL" else 0.0)
        CONTROL_STATUS.labels(control_id=c.control_id, tier=c.tier, source_lab=c.source_lab).set(c_val)
        if c.freshness_seconds is not None:
            CONTROL_FRESHNESS.labels(control_id=c.control_id).set(c.freshness_seconds)
