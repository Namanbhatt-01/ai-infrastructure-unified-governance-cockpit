# 🏛️ Tier 6: Unified AI Infrastructure Operations & Governance Cockpit (Capstone)

[![CI/CD Pipeline](https://github.com/Namanbhatt-01/ai-infrastructure-unified-governance-cockpit/actions/workflows/unified_cockpit_ci.yml/badge.svg)](https://github.com/Namanbhatt-01/ai-infrastructure-unified-governance-cockpit/actions/workflows/unified_cockpit_ci.yml)
[![Release](https://img.shields.io/badge/Release-v1.0.0-blue.svg)](https://github.com/Namanbhatt-01/ai-infrastructure-unified-governance-cockpit/releases/tag/v1.0.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Footprint](https://img.shields.io/badge/Memory%20Footprint-~1.0%20GB%20RAM-success.svg)](docker-compose.yml)
[![Cisco NDB / Splunk Equivalent](https://img.shields.io/badge/Architecture-Cisco%20NDB%20%2F%20Splunk%20ITSI-purple.svg)](docs/cisco_ndb_splunk_comparative_memo.md)

An enterprise-grade, single-pane-of-glass operational telemetry cockpit and governance platform synthesizing all 5 underlying AI data center infrastructure tiers on a **₹0 software budget**, optimized for **Apple Silicon (M1 ARM64)** and standard developer workstations.

---

## 📌 Executive Architecture & Multi-Tier Synthesis

This Capstone project synthesizes the entire portfolio into an integrated operational command center:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               TIER 6: UNIFIED SINGLE-PANE-OF-GLASS GOVERNANCE COCKPIT                  │
│               (Grafana :3000 | FastAPI Aggregator :8080 | Prometheus :9090)            │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Correlated Multi-Tier Telemetry Stream
    ┌───────────────────┬───────────────────┼───────────────────┬───────────────────┐
    ▼                   ▼                   ▼                   ▼                   ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│    TIER 1    │ │    TIER 2    │ │    TIER 3    │ │    TIER 4    │ │    TIER 5    │
│ Lossless AI  │ │  NetDevOps   │ │ Hybrid Cloud │ │  AI SecOps   │ │  Zero-Trust  │
│    Fabric    │ │    CI/CD     │ │  Assurance   │ │  SIEM (Zeek) │ │ RAG Security │
├──────────────┤ ├──────────────┤ ├──────────────┤ ├──────────────┤ ├──────────────┤
│ • RoCEv2     │ │ • GitOps IaC │ │ • Synthetic  │ │ • Rogue LLM  │ │ • Qdrant DB  │
│ • ECN WRED   │ │ • PyTest     │ │   Blackbox   │ │   Detection  │ │ • RBAC Pre-  │
│ • PFC Head-  │ │ • Config     │ │ • Hop Latency│ │ • Suricata   │ │   Filtering  │
│   room Sizing│ │   Drift Auto-│ │ • Cloud SLO  │ │   Egress Flow│ │ • Prompt Inj.│
│ • Incast Obs.│ │   Remediate  │ │   Monitoring │ │   Alerts     │ │   Guardrails │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

---

## 🎯 Six-Tier Portfolio Integration Matrix

| Tier & Subsystem | Core Protocol / Framework | Integrated Lab Project | Operational Telemetry & Health Signals |
| :--- | :--- | :--- | :--- |
| **Tier 1: AI Compute Fabric** | RoCEv2, ECN (RFC 3168), PFC (802.1Qbb) | [Lossless Fabric Lab](https://github.com/Namanbhatt-01/lossless-ai-fabric-emulation-lab) | Switch buffer queue depths, ECN marking rates, PFC pause frame counts. |
| **Tier 2: NetDevOps Automation** | GitOps, Scrapli, Pytest, GitHub CI | [NetDevOps CI/CD Lab](https://github.com/Namanbhatt-01/netdevops-cicd-pipeline-lab) | CI/CD run velocity, automated state assertions, configuration drift remediations. |
| **Tier 3: Hybrid Cloud Assurance** | Prometheus Blackbox, ICMP, TCP, HTTP | [Hybrid Cloud Assurance Lab](https://github.com/Namanbhatt-01/hybrid-cloud-assurance-telemetry-lab) | Multi-cloud AI endpoint latency (P99), DNS lookup time, hop jitter, SLO availability %. |
| **Tier 4: Enterprise AI SecOps** | Wazuh SIEM, OpenSearch, Zeek, Suricata | [SIEM Security Lab](https://github.com/Namanbhatt-01/siem-security-ai-workloads-lab) | Active threat counters, rogue LLM data exfiltration alerts, egress flow anomalies. |
| **Tier 5: Zero-Trust RAG Security** | Qdrant Rust OSS, RBAC Pre-Filter, Bandit | [Zero-Trust RAG Lab](https://github.com/Namanbhatt-01/zero-trust-ai-rag-security-lab) | Cross-tenant chunk isolation (0 leaks), prompt injection blocks (400), PII redactions. |
| **Tier 6: Unified Ops & Governance** | Grafana 10.2, Prometheus TSDB, FastAPI | **Current Capstone Repository** | Single-pane cockpit correlating all tiers into unified KPIs & compliance scores. |

---

## 🚀 Quickstart & Local Reproduction

### 1. Launch the Unified Operations Stack
```bash
# Start Aggregator, Prometheus, and Grafana in background
make up
```

### 2. Verify Service Endpoints
- **Grafana Cockpit Dashboard**: [http://localhost:3000](http://localhost:3000) *(Anonymous Admin enabled)*
- **Prometheus TSDB Engine**: [http://localhost:9090](http://localhost:9090)
- **FastAPI Telemetry Aggregator**: [http://localhost:8080/docs](http://localhost:8080/docs)
- **Executive Summary API**: [http://localhost:8080/api/v1/cockpit-summary](http://localhost:8080/api/v1/cockpit-summary)

### 3. Run Automated Verification Suite
```bash
python3 verify_unified_cockpit.py
```

### 4. Teardown
```bash
make down
```

---

## 📊 Live Verification & Testbed Assertions

```text
================================================================================
      TIER 6: UNIFIED AI INFRASTRUCTURE OPERATIONS & GOVERNANCE AUDIT       
================================================================================
  [✅ PASS] Aggregator Service Health & Readiness
  [✅ PASS] Executive Single-Pane-of-Glass Summary API
  [✅ PASS] Dynamic Cross-Tier Telemetry Ingestion
  [✅ PASS] Prometheus TSDB Metric Scrape & Indexing
  [✅ PASS] Grafana Provisioned Single-Pane Dashboard
================================================================================
🎉 ALL TIER 6 CAPSTONE INTEGRATION ASSERTIONS VERIFIED SUCCESSFULLY!
```

---

## 📚 Technical Documentation & Architecture Memos

- **Capstone Architecture Whitepaper**: [`docs/unified_ai_infrastructure_architecture_whitepaper.md`](docs/unified_ai_infrastructure_architecture_whitepaper.md)
- **Cisco NDB & Splunk Comparative Engineering Memo**: [`docs/cisco_ndb_splunk_comparative_memo.md`](docs/cisco_ndb_splunk_comparative_memo.md)
- **Real-Time Execution Evidence**: [`poc/REALTIME_EVIDENCE.md`](poc/REALTIME_EVIDENCE.md)

---

## 📜 License
This project is licensed under the [MIT License](LICENSE).
