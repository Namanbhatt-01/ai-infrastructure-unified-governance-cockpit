# LAB 07: Unified AI Infrastructure Control Plane

[![CI/CD Pipeline](https://github.com/Namanbhatt-01/ai-infrastructure-unified-governance-cockpit/actions/workflows/unified_cockpit_ci.yml/badge.svg)](https://github.com/Namanbhatt-01/ai-infrastructure-unified-governance-cockpit/actions/workflows/unified_cockpit_ci.yml)
[![Release](https://img.shields.io/badge/Release-v1.0.0-blue.svg)](https://github.com/Namanbhatt-01/ai-infrastructure-unified-governance-cockpit/releases/tag/v1.0.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Footprint](https://img.shields.io/badge/Memory%20Footprint-~1.0%20GB%20RAM-success.svg)](docker-compose.yml)

A reproducible reference architecture for evidence-based infrastructure governance and control plane aggregation. This system synthesizes telemetry, validation outputs, and security assertions across the 6 underlying technical labs using machine-readable evidence contracts rather than simulated dashboard metrics.

---

## 1. Problem Statement & Architecture

In large-scale AI infrastructure deployments, individual operational tools (switch telemetry collectors, CI/CD validators, blackbox path probers, SIEM analyzers, and vector database guardrails) operate as isolated silos. Traditional dashboard aggregators often mask outages by displaying synthetic averages or hardcoded "healthy" states.

This project implements an **Evidence-Driven Control Plane**:
1. It does not synthesize artificial operational truth.
2. It consumes signed, machine-readable evidence envelopes (`EvidenceRecord`) emitted by underlying systems.
3. It evaluates controls against explicit freshness Service Level Objectives (SLOs) and assertion outcomes.
4. It derives explainable governance posture states: `PASS`, `DEGRADED`, `UNKNOWN`, `STALE`, or `FAIL`.

```
                    ┌────────────────────────────────────────┐
                    │     LAB 07: UNIFIED CONTROL PLANE      │
                    │   FastAPI Aggregator & Engine (:8080)  │
                    │   Prometheus TSDB (:9090)              │
                    │   Grafana Single-Pane Dashboard (:3000)│
                    └───────────────────▲────────────────────┘
                                        │
                         HTTP Evidence Ingestion API
                         POST /api/v1/evidence/ingest
                                        │
    ┌───────────────┬───────────────────┼───────────────────┬───────────────┐
    │               │                   │                   │               │
┌───┴──────────┐ ┌──┴────────────┐ ┌────┴────────────┐ ┌────┴────────────┐ ┌───┴────────────┐
│    LAB 01    │ │    LAB 02     │ │    LAB 03       │ │    LAB 04       │ │   LAB 05 / 06   │
│ Lossless AI  │ │  NetDevOps    │ │  Hybrid Cloud   │ │  AI SIEM SecOps │ │ Telemetry Ingest│
│    Fabric    │ │  CI/CD Drift  │ │  Path Assurance │ │  Threat Defense │ │ Zero-Trust RAG  │
└──────────────┘ └───────────────┘ └─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## 2. Six-Tier Control Catalog & Evidence Mapping

| Control ID | Governance Control Name | Target Lab | Freshness SLO | Evaluated Invariant |
| :--- | :--- | :--- | :--- | :--- |
| **`FABRIC-001`** | Lossless Queue & ECN Congestion | [Lab 01 (Lossless Fabric)](https://github.com/Namanbhatt-01/lossless-ai-fabric-emulation-lab) | 300s | Queue depth strictly below headroom threshold; zero uncontrolled packet drop. |
| **`NET-002`** | GitOps Change Validation & Drift | [Lab 02 (NetDevOps CI/CD)](https://github.com/Namanbhatt-01/netdevops-cicd-pipeline-lab) | 300s | 100% automated state assertion pass rate on pre-deployment validation. |
| **`CLOUD-003`** | Hybrid Cloud Endpoint Latency SLO | [Lab 03 (Hybrid Cloud Assurance)](https://github.com/Namanbhatt-01/hybrid-cloud-assurance-telemetry-lab) | 300s | Multi-cloud inference probe P99 RTT < 50ms; synthetic availability >= 99.5%. |
| **`SIEM-004`** | AI SecOps Threat Detection | [Lab 04 (SIEM AI Security)](https://github.com/Namanbhatt-01/siem-security-ai-workloads-lab) | 300s | Zero unmitigated vector DB exfiltration bursts or rogue GPU egress anomalies. |
| **`TEL-005`** | High-Frequency Telemetry Pipeline | [Lab 05 (High-Frequency Telemetry)](https://github.com/Namanbhatt-01/high-frequency-telemetry-ingestion-lab) | 300s | Buffer telemetry streaming cadence <= 100ms; zero collector pipeline drops. |
| **`RAG-006`** | Zero-Trust RAG Policy & Isolation | [Lab 06 (Zero-Trust RAG)](https://github.com/Namanbhatt-01/zero-trust-ai-rag-security-lab) | 300s | Zero cross-tenant chunk retrieval leaks across all evaluation queries. |

---

## 3. Evidence Envelope Specification

Every underlying technical laboratory produces evidence matching the canonical JSON schema:

```json
{
  "schema_version": "1.0",
  "experiment": {
    "id": "rag-security-001",
    "name": "Zero-Trust Retrieval Isolation and Policy Invariants"
  },
  "execution": {
    "run_id": "run-20260929-1420",
    "timestamp": "2026-09-29T14:20:00Z",
    "environment": "docker-compose",
    "platform": "darwin-arm64"
  },
  "measurements": [
    { "metric": "cross_tenant_chunks_leaked", "value": 0, "target": 0, "mode": "measured" }
  ],
  "assertions": [
    { "id": "RAG-SEC-001", "name": "Cross-Tenant Vector Isolation Invariant", "passed": true }
  ],
  "result": "passed"
}
```

---

## 4. State Transition & Evaluation Engine

The evaluation engine computes governance state using deterministic rules:
- **`UNKNOWN`**: No evidence has been ingested for this control.
- **`STALE`**: Last ingested evidence exceeds `freshness_slo_seconds`.
- **`FAIL`**: Evidence contains one or more failed assertions (`passed: false`).
- **`PASS`**: Ingested within SLO window and all assertions verified.

---

## 5. Quickstart & Local Reproduction

### Prerequisites
- Docker & Docker Compose (or OrbStack on macOS)
- Python 3.11+

### Step 1: Start the Control Plane Stack
```bash
make up
```

### Step 2: Verify Endpoints
- **Grafana Dashboard**: [http://localhost:3000](http://localhost:3000) *(Anonymous Admin enabled)*
- **Prometheus TSDB**: [http://localhost:9090](http://localhost:9090)
- **FastAPI Control Plane API**: [http://localhost:8080/docs](http://localhost:8080/docs)
- **Governance Posture Summary**: [http://localhost:8080/api/v1/summary](http://localhost:8080/api/v1/summary)

### Step 3: Run the Verification Suite
```bash
python3 verify_unified_cockpit.py
```

### Step 4: Teardown
```bash
make down
```

---

## 6. Known Limitations

1. **Transport Boundary**: Evidence ingestion is currently implemented via HTTP POST and static file seed loading; production environments would utilize authenticated mTLS, gRPC streams, or Apache Kafka topics.
2. **Persistence Boundary**: Control catalog state and ingested records are stored in-memory with file backup, rather than a persistent relational database like PostgreSQL.
3. **Cryptographic Signatures**: Evidence envelopes include execution metadata (run ID, platform, timestamp) but currently lack asymmetric cryptographic signature verification (Ed25519/X.509).

---

## 7. License

MIT License. See [LICENSE](LICENSE) for details.
