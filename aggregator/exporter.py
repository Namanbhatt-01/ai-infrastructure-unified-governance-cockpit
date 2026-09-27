from prometheus_client import Gauge, Counter, Histogram

# ==============================================================================
# TIER 1 & HIGH-FREQ TELEMETRY: LOSSLESS FABRIC & SWITCH BUFFER QUEUES
# ==============================================================================
FABRIC_HEALTH = Gauge('ai_fabric_cluster_health_status', '0 = Optimal, 1 = Degraded')
QUEUE_DEPTH = Gauge('ai_fabric_queue_depth_bytes', 'Switch shared buffer occupancy in bytes', ['queue'])
ECN_KMIN_THRESHOLD = Gauge('ai_fabric_ecn_kmin_threshold_bytes', 'ECN WRED early marking threshold bytes')
PFC_PAUSE_THRESHOLD = Gauge('ai_fabric_pfc_headroom_threshold_bytes', 'PFC pause frame threshold bytes')
ECN_MARKED_PKTS = Counter('ai_fabric_ecn_marked_packets_total', 'Cumulative ECN Congestion Experienced (CE) marked packets')
PFC_PAUSE_FRAMES = Counter('ai_fabric_pfc_pause_frames_total', 'Cumulative IEEE 802.1Qbb PFC pause frames transmitted')

# ==============================================================================
# TIER 2: NETDEVOPS GITOPS AUTOMATION & CONFIGURATION DRIFT
# ==============================================================================
NETDEVOPS_PIPELINE_RUNS = Counter('ai_netdevops_cicd_pipeline_runs_total', 'Total CI/CD pipeline executions')
NETDEVOPS_DRIFT_EVENTS = Counter('ai_netdevops_config_drift_events_total', 'Automated configuration drift remediation events')
NETDEVOPS_PYTEST_ASSERTIONS = Counter('ai_netdevops_pytest_passed_assertions_total', 'Total passing pytest network state assertions')

# ==============================================================================
# TIER 3: HYBRID MULTI-CLOUD SYNTHETIC PATH ASSURANCE
# ==============================================================================
SYNTHETIC_PATH_LATENCY = Gauge('ai_synthetic_path_latency_ms', 'Synthetic probe round-trip latency in ms', ['target'])
ENDPOINT_AVAILABILITY = Gauge('ai_endpoint_synthetic_availability_percent', 'Synthetic endpoint SLO availability percentage')

# ==============================================================================
# TIER 4: AI SECOPS SIEM & BEHAVIORAL THREAT MONITORING
# ==============================================================================
SECOPS_ACTIVE_THREATS = Gauge('ai_secops_active_security_threats', 'Active unmitigated threat alerts', ['severity'])
SECOPS_EXFILTRATION_BURSTS = Counter('ai_secops_rogue_exfiltration_bursts_total', 'Rogue LLM exfiltration attempt alerts')
SECOPS_INJECTIONS_DETECTED = Counter('ai_secops_prompt_injections_detected_total', 'SIEM detected prompt injection signatures')
SECOPS_SURICATA_ANOMALIES = Counter('ai_secops_suricata_flow_anomalies_total', 'Suricata anomalous flow triggers')

# ==============================================================================
# TIER 5: ZERO-TRUST RAG RBAC & GUARDRAIL ENFORCEMENT
# ==============================================================================
RAG_CROSS_TENANT_LEAKS = Gauge('ai_rag_cross_tenant_leaks_total', 'Total detected cross-tenant vector chunk leaks (Target: 0)')
RAG_PROMPT_INJECTIONS_BLOCKED = Counter('ai_rag_prompt_injections_blocked_total', 'OWASP LLM01 Injections Blocked (400 Bad Request)')
RAG_PII_REDACTIONS = Counter('ai_rag_pii_redactions_total', 'OWASP LLM02 Ingestion PII/PCI Redactions')
RAG_UNAUTH_BLOCKS = Counter('ai_rag_unauthenticated_blocks_total', 'OWASP LLM06 Unauthenticated Access Rejections (401/403)')

# ==============================================================================
# TIER 6: GOVERNANCE, COMPLIANCE & CAPSTONE SLA POSTURE
# ==============================================================================
GOVERNANCE_COMPLIANCE_SCORE = Gauge('ai_governance_compliance_score', 'NIST AI RMF / SOC 2 Compliance Score Percentage')

def initialize_defaults():
    FABRIC_HEALTH.set(0)
    ECN_KMIN_THRESHOLD.set(65536)     # 64 KB
    PFC_PAUSE_THRESHOLD.set(196608)   # 192 KB
    ENDPOINT_AVAILABILITY.set(99.98)
    RAG_CROSS_TENANT_LEAKS.set(0)
    GOVERNANCE_COMPLIANCE_SCORE.set(100.0)
    
    # Initialize basic gauges
    QUEUE_DEPTH.labels(queue='q3_rocev2_lossless').set(18400)
    QUEUE_DEPTH.labels(queue='q0_best_effort').set(4200)
    SYNTHETIC_PATH_LATENCY.labels(target='inference-us-east').set(28.4)
    SYNTHETIC_PATH_LATENCY.labels(target='inference-eu-west').set(74.2)
    SYNTHETIC_PATH_LATENCY.labels(target='local-ollama-cluster').set(3.1)
    SECOPS_ACTIVE_THREATS.labels(severity='high').set(0)
    SECOPS_ACTIVE_THREATS.labels(severity='medium').set(0)
