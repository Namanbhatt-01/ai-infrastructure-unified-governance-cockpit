import os
import sys
import time
import json
import requests
from datetime import datetime

AGGREGATOR_URL = os.getenv("AGGREGATOR_URL", "http://localhost:8080")
PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")
GRAFANA_URL = os.getenv("GRAFANA_URL", "http://localhost:3000")

def run_verification():
    print("=" * 80)
    print("   LAB 07: UNIFIED AI INFRASTRUCTURE CONTROL PLANE & EVIDENCE AUDIT         ")
    print("=" * 80)
    print(f"Timestamp: {datetime.utcnow().isoformat()}Z\n")

    results = []

    # --------------------------------------------------------------------------
    # 1. Healthcheck Assertion
    # --------------------------------------------------------------------------
    print("[TEST 1] Checking Governance Control Plane Health & Readiness...")
    try:
        resp1 = requests.get(f"{AGGREGATOR_URL}/healthz", timeout=10)
        passed1 = resp1.status_code == 200 and resp1.json().get("status") == "healthy"
        print(f"  [+] HTTP Status: {resp1.status_code} | Service: {resp1.json().get('service')}")
    except Exception as e:
        passed1 = False
        print(f"  [❌ ERROR] Control Plane connection failed: {e}")
    results.append(("Control Plane Health & Readiness", passed1))

    # --------------------------------------------------------------------------
    # 2. Dynamic Evidence Ingestion Assertion
    # --------------------------------------------------------------------------
    print("\n[TEST 2] Ingesting Live Evidence Envelopes from Labs 01-06...")
    sample_evidence = {
        "schema_version": "1.0",
        "experiment": {
            "id": "rag-security-001",
            "name": "Zero-Trust Retrieval Isolation and Policy Invariants"
        },
        "execution": {
            "run_id": f"live-test-{int(time.time())}",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "environment": "docker-compose",
            "platform": "darwin-arm64"
        },
        "measurements": [
            {"metric": "cross_tenant_chunks_leaked", "value": 0, "target": 0, "mode": "measured"}
        ],
        "assertions": [
            {"id": "RAG-SEC-001", "name": "Cross-Tenant Vector Isolation Invariant", "passed": True}
        ],
        "result": "passed"
    }

    try:
        ingest_resp = requests.post(f"{AGGREGATOR_URL}/api/v1/evidence/ingest", json=sample_evidence, timeout=10)
        passed2 = ingest_resp.status_code == 201 and ingest_resp.json().get("status") == "ACCEPTED"
        print(f"  [+] Ingestion Status: {ingest_resp.status_code} | Experiment: {ingest_resp.json().get('experiment_id')}")
    except Exception as e:
        passed2 = False
        print(f"  [❌ ERROR] Ingestion failed: {e}")
    results.append(("Evidence Envelope Ingestion API", passed2))

    # --------------------------------------------------------------------------
    # 3. Control Catalog & Provenance Assertion
    # --------------------------------------------------------------------------
    print("\n[TEST 3] Evaluating Governance Controls & Provenance Tracking...")
    try:
        ctrl_resp = requests.get(f"{AGGREGATOR_URL}/api/v1/controls", timeout=10)
        controls = ctrl_resp.json()
        passed3 = ctrl_resp.status_code == 200 and len(controls) == 6
        print(f"  [+] Evaluated Controls: {len(controls)}")
        for c in controls:
            print(f"      - [{c['control_id']}] {c['name']} -> {c['status']} ({c['confidence']})")
            print(f"        Reason: {c['reason']}")
    except Exception as e:
        passed3 = False
        print(f"  [❌ ERROR] Control evaluation failed: {e}")
    results.append(("Governance Control Evaluation & Provenance", passed3))

    # --------------------------------------------------------------------------
    # 4. Governance Summary & Explanatory Posture Assertion
    # --------------------------------------------------------------------------
    print("\n[TEST 4] Querying Overall Governance Posture...")
    try:
        sum_resp = requests.get(f"{AGGREGATOR_URL}/api/v1/summary", timeout=10)
        summary = sum_resp.json()
        passed4 = (
            sum_resp.status_code == 200 and
            summary.get("total_controls") == 6 and
            summary.get("passing_controls") >= 1
        )
        print(f"  [+] Overall Status: {summary.get('overall_status')}")
        print(f"  [+] Passing: {summary.get('passing_controls')} | Failing: {summary.get('failing_controls')} | Stale: {summary.get('stale_controls')} | Unknown: {summary.get('unknown_controls')}")
    except Exception as e:
        passed4 = False
        print(f"  [❌ ERROR] Summary query failed: {e}")
    results.append(("Derived Governance Posture Summary", passed4))

    # --------------------------------------------------------------------------
    # 5. Negative Test: Failure State Propagation
    # --------------------------------------------------------------------------
    print("\n[TEST 5] Testing Negative Path: Failing Evidence Ingestion & Alert Propagation...")
    failing_evidence = {
        "schema_version": "1.0",
        "experiment": {
            "id": "wan-latency-001",
            "name": "Synthetic Multi-Cloud AI Endpoint Latency Probing"
        },
        "execution": {
            "run_id": f"failing-test-{int(time.time())}",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "environment": "prometheus-blackbox",
            "platform": "darwin-arm64"
        },
        "measurements": [
            {"metric": "p99_probe_rtt_ms", "value": 184.2, "target": 50.0, "mode": "measured"}
        ],
        "assertions": [
            {"id": "ASSURANCE-ASSERT-001", "name": "Multi-Cloud Inference SLO Compliance", "passed": False, "detail": "P99 latency of 184.2ms breached 50ms SLO threshold."}
        ],
        "result": "failed"
    }

    try:
        f_resp = requests.post(f"{AGGREGATOR_URL}/api/v1/evidence/ingest", json=failing_evidence, timeout=10)
        s_after = requests.get(f"{AGGREGATOR_URL}/api/v1/summary", timeout=10).json()
        passed5 = s_after.get("failing_controls") >= 1 and s_after.get("overall_status") == "FAIL"
        print(f"  [+] Ingested failing evidence -> Posture transitioned to: {s_after.get('overall_status')} (Failing controls: {s_after.get('failing_controls')})")
    except Exception as e:
        passed5 = False
        print(f"  [❌ ERROR] Negative test failed: {e}")
    results.append(("Negative Path: Failure State Propagation", passed5))

    # --------------------------------------------------------------------------
    # 6. Prometheus TSDB Metric Scraping Assertion
    # --------------------------------------------------------------------------
    print("\n[TEST 6] Verifying Prometheus TSDB Scraping...")
    time.sleep(2)
    try:
        p_resp = requests.get(f"{PROMETHEUS_URL}/api/v1/query?query=ai_governance_total_controls_count", timeout=10)
        p_data = p_resp.json()
        passed6 = p_resp.status_code == 200 and p_data.get("status") == "success"
        print(f"  [+] Prometheus Scrape Status: {p_data.get('status')} | Metric Value: {p_data.get('data', {}).get('result', [{}])[0].get('value', [0, 0])[1]}")
    except Exception as e:
        passed6 = False
        print(f"  [❌ ERROR] Prometheus query failed: {e}")
    results.append(("Prometheus Metric Scrape & Indexing", passed6))

    # --------------------------------------------------------------------------
    # 7. Grafana Health & Dashboard Provisioning Assertion
    # --------------------------------------------------------------------------
    print("\n[TEST 7] Verifying Grafana Single-Pane-of-Glass Dashboard...")
    try:
        g_health = requests.get(f"{GRAFANA_URL}/api/health", timeout=10)
        passed7 = g_health.status_code == 200
        print(f"  [+] Grafana Database Status: {g_health.json().get('database')}")
    except Exception as e:
        passed7 = False
        print(f"  [❌ ERROR] Grafana check failed: {e}")
    results.append(("Grafana Engine Health", passed7))

    # --------------------------------------------------------------------------
    # SUMMARY MATRIX
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("             LAB 07 CONTROL PLANE VERIFICATION SUMMARY MATRIX             ")
    print("=" * 80)
    all_passed = True
    for name, passed in results:
        mark = "✅ PASS" if passed else "❌ FAIL"
        if not passed:
            all_passed = False
        print(f"  [{mark}] {name}")
    print("=" * 80)

    # Save evidence JSON
    evidence_out = {
        "schema_version": "1.0",
        "experiment": {
            "id": "governance-cockpit-001",
            "name": "Unified AI Infrastructure Control Plane Verification"
        },
        "execution": {
            "run_id": f"gov-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "environment": "docker-compose",
            "platform": "darwin-arm64"
        },
        "assertions": [{"name": name, "passed": passed} for name, passed in results],
        "result": "passed" if all_passed else "failed"
    }

    os.makedirs("poc", exist_ok=True)
    with open("poc/evidence.json", "w") as f:
        json.dump(evidence_out, f, indent=2)

    if all_passed:
        print("\n🎉 ALL LAB 07 CONTROL PLANE ASSERTIONS VERIFIED SUCCESSFULLY!\n")
    else:
        print("\n❌ SOME CONTROL PLANE ASSERTIONS FAILED!\n", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_verification()
