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
    print("      TIER 6: UNIFIED AI INFRASTRUCTURE OPERATIONS & GOVERNANCE AUDIT       ")
    print("=" * 80)
    print(f"Timestamp: {datetime.utcnow().isoformat()}Z\n")

    results = []

    # --------------------------------------------------------------------------
    # 1. Healthcheck Assertion
    # --------------------------------------------------------------------------
    print("[TEST 1] Checking Unified Cockpit Aggregator Health & Readiness...")
    try:
        resp1 = requests.get(f"{AGGREGATOR_URL}/healthz", timeout=10)
        passed1 = resp1.status_code == 200 and resp1.json().get("status") == "healthy"
        print(f"  [+] HTTP Status: {resp1.status_code} | Service: {resp1.json().get('service')}")
    except Exception as e:
        passed1 = False
        print(f"  [❌ ERROR] Aggregator connection failed: {e}")
    results.append(("Aggregator Service Health & Readiness", passed1))

    # --------------------------------------------------------------------------
    # 2. Executive Cockpit Summary Assertion
    # --------------------------------------------------------------------------
    print("\n[TEST 2] Querying Single-Pane-of-Glass Executive Summary...")
    try:
        resp2 = requests.get(f"{AGGREGATOR_URL}/api/v1/cockpit-summary", timeout=10)
        data2 = resp2.json()
        passed2 = (
            resp2.status_code == 200 and 
            data2.get("fabric_status") == "OPTIMAL" and
            data2.get("cross_tenant_leaks") == 0 and
            data2.get("compliance_score_percent") == 100.0
        )
        print(f"  [+] Fabric Status: {data2.get('fabric_status')} | Cross-Tenant Leaks: {data2.get('cross_tenant_leaks')}")
        print(f"  [+] Multi-Cloud SLO Availability: {data2.get('slo_availability_percent')}% | Compliance Score: {data2.get('compliance_score_percent')}%")
        for tier, status in data2.get("tier_health", {}).items():
            print(f"      - {tier}: {status}")
    except Exception as e:
        passed2 = False
        print(f"  [❌ ERROR] Cockpit summary query failed: {e}")
    results.append(("Executive Single-Pane-of-Glass Summary API", passed2))

    # --------------------------------------------------------------------------
    # 3. Dynamic Cross-Tier Telemetry Ingestion Assertion
    # --------------------------------------------------------------------------
    print("\n[TEST 3] Ingesting Dynamic Cross-Tier Telemetry Events...")
    test_events = [
        {"tier": "tier1_fabric", "metric_name": "queue_depth", "value": 72400.0, "labels": {"queue": "q3_rocev2_lossless"}},
        {"tier": "tier3_assurance", "metric_name": "path_latency", "value": 31.5, "labels": {"target": "inference-us-east"}},
        {"tier": "tier4_secops", "metric_name": "rogue_exfiltration_burst", "value": 1.0, "labels": {}},
        {"tier": "tier5_rag", "metric_name": "prompt_injection_blocked", "value": 1.0, "labels": {}}
    ]
    ingest_passed = True
    for ev in test_events:
        try:
            r = requests.post(f"{AGGREGATOR_URL}/api/v1/telemetry/ingest", json=ev, timeout=10)
            if r.status_code != 201:
                ingest_passed = False
        except Exception:
            ingest_passed = False
    print(f"  [+] Ingested {len(test_events)} cross-tier telemetry events -> Status: {'SUCCESS' if ingest_passed else 'FAILED'}")
    results.append(("Dynamic Cross-Tier Telemetry Ingestion", ingest_passed))

    # --------------------------------------------------------------------------
    # 4. Prometheus TSDB Ingestion & Scrape Target Verification
    # --------------------------------------------------------------------------
    print("\n[TEST 4] Verifying Prometheus TSDB Scraping & Metric Retention...")
    time.sleep(3) # allow 1 scrape interval
    try:
        p_resp = requests.get(f"{PROMETHEUS_URL}/api/v1/query?query=ai_fabric_cluster_health_status", timeout=10)
        p_data = p_resp.json()
        passed4 = p_resp.status_code == 200 and p_data.get("status") == "success" and len(p_data.get("data", {}).get("result", [])) > 0
        print(f"  [+] Prometheus Scrape Status: {p_data.get('status')} | Indexed Series Count: {len(p_data.get('data', {}).get('result', []))}")
    except Exception as e:
        passed4 = False
        print(f"  [❌ ERROR] Prometheus query failed: {e}")
    results.append(("Prometheus TSDB Metric Scrape & Indexing", passed4))

    # --------------------------------------------------------------------------
    # 5. Grafana Single-Pane-of-Glass Dashboard Provisioning Assertion
    # --------------------------------------------------------------------------
    print("\n[TEST 5] Verifying Grafana Dashboard Provisioning & Health...")
    try:
        g_health = requests.get(f"{GRAFANA_URL}/api/health", timeout=10)
        g_dash = requests.get(f"{GRAFANA_URL}/api/dashboards/uid/ai-infra-cockpit-single-pane", timeout=10)
        passed5 = g_health.status_code == 200 and g_dash.status_code == 200
        print(f"  [+] Grafana Health Status: {g_health.json().get('database')} | Provisioned Dashboard Title: {g_dash.json().get('dashboard', {}).get('title')}")
    except Exception as e:
        passed5 = False
        print(f"  [❌ ERROR] Grafana verification failed: {e}")
    results.append(("Grafana Provisioned Single-Pane Dashboard", passed5))

    # --------------------------------------------------------------------------
    # SUMMARY MATRIX
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("          TIER 6 UNIFIED COCKPIT VERIFICATION SUMMARY MATRIX              ")
    print("=" * 80)
    all_passed = True
    for name, passed in results:
        mark = "✅ PASS" if passed else "❌ FAIL"
        if not passed:
            all_passed = False
        print(f"  [{mark}] {name}")
    print("=" * 80)

    # Save evidence JSON
    evidence = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "lab": "Tier 6: Unified AI Infrastructure Operations & Governance Cockpit",
        "overall_status": "PASSED" if all_passed else "FAILED",
        "results": [{"test": name, "passed": passed} for name, passed in results]
    }
    os.makedirs("poc", exist_ok=True)
    with open("poc/live_unified_cockpit_evidence.json", "w") as f:
        json.dump(evidence, f, indent=2)

    if all_passed:
        print("\n🎉 ALL TIER 6 CAPSTONE INTEGRATION ASSERTIONS VERIFIED SUCCESSFULLY!\n")
    else:
        print("\n❌ SOME TIER 6 COCKPIT ASSERTIONS FAILED!\n", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_verification()
