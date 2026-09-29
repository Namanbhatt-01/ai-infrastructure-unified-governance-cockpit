import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from models import EvidenceRecord, ControlFinding, GovernancePosture, ControlStatusType

# Standard Governance Control Catalog across 6 Technical Labs
CONTROL_CATALOG = [
    {
        "control_id": "FABRIC-001",
        "name": "Lossless Queue Integrity & ECN Early Marking",
        "tier": "Tier 1: AI Compute Fabric",
        "source_lab": "LAB 01 (Lossless Fabric Emulation)",
        "freshness_slo_seconds": 600
    },
    {
        "control_id": "NET-002",
        "name": "NetDevOps Configuration Drift & Automated Assertion",
        "tier": "Tier 2: NetDevOps Automation",
        "source_lab": "LAB 02 (NetDevOps Change Validation)",
        "freshness_slo_seconds": 600
    },
    {
        "control_id": "ASSURANCE-003",
        "name": "Synthetic Multi-Cloud AI Path Latency & SLO",
        "tier": "Tier 3: Hybrid Cloud Assurance",
        "source_lab": "LAB 03 (Hybrid Cloud Path Assurance)",
        "freshness_slo_seconds": 300
    },
    {
        "control_id": "SECOPS-004",
        "name": "SIEM Threat Detection & Rogue Exfiltration Guard",
        "tier": "Tier 4: Enterprise AI SecOps",
        "source_lab": "LAB 04 (AI Workload Security SIEM)",
        "freshness_slo_seconds": 300
    },
    {
        "control_id": "TELEMETRY-005",
        "name": "Sub-Second Push Telemetry & Microburst Capture",
        "tier": "Tier 5: High-Frequency Telemetry",
        "source_lab": "LAB 05 (High-Frequency Fabric Telemetry)",
        "freshness_slo_seconds": 300
    },
    {
        "control_id": "RAG-006",
        "name": "Zero-Trust Retrieval Isolation & PII Protection",
        "tier": "Tier 6: Zero-Trust RAG Security",
        "source_lab": "LAB 06 (Zero-Trust RAG Security)",
        "freshness_slo_seconds": 300
    }
]

class ControlEvaluationEngine:
    """Consumes machine-readable evidence records from Labs 01-06,
    evaluates control pass/fail criteria, tracks freshness SLOs,
    and derives explainable governance posture with provenance."""

    def __init__(self):
        self.evidence_store: Dict[str, EvidenceRecord] = {}
        self.last_ingested_at: Dict[str, datetime] = {}

    def ingest_evidence(self, evidence: EvidenceRecord) -> Dict[str, str]:
        """Validates and stores incoming evidence record by experiment ID."""
        exp_id = evidence.experiment.id
        self.evidence_store[exp_id] = evidence
        self.last_ingested_at[exp_id] = datetime.utcnow()
        return {
            "status": "ACCEPTED",
            "experiment_id": exp_id,
            "run_id": evidence.execution.run_id,
            "assertions_count": str(len(evidence.assertions)),
            "result": evidence.result
        }

    def evaluate_controls(self) -> List[ControlFinding]:
        """Evaluates all registered controls against current evidence and freshness."""
        now = datetime.utcnow()
        findings = []

        # Mapping of Control ID to expected Experiment ID
        control_exp_map = {
            "FABRIC-001": "fabric-queue-001",
            "NET-002": "netdevops-ci-001",
            "ASSURANCE-003": "wan-latency-001",
            "SECOPS-004": "siem-threat-001",
            "TELEMETRY-005": "telemetry-incast-001",
            "RAG-006": "rag-security-001"
        }

        for c in CONTROL_CATALOG:
            cid = c["control_id"]
            exp_id = control_exp_map.get(cid, "")
            evidence = self.evidence_store.get(exp_id)
            last_time = self.last_ingested_at.get(exp_id)
            slo = c["freshness_slo_seconds"]

            if not evidence or not last_time:
                # No evidence received yet -> UNKNOWN
                findings.append(ControlFinding(
                    control_id=cid,
                    name=c["name"],
                    tier=c["tier"],
                    source_lab=c["source_lab"],
                    status="UNKNOWN",
                    last_observed=None,
                    freshness_seconds=None,
                    freshness_slo_seconds=slo,
                    evidence_run_id=None,
                    confidence="unverified",
                    reason="No evidence received from source laboratory pipeline."
                ))
                continue

            freshness = int((now - last_time).total_seconds())

            if freshness > slo:
                # Evidence is STALE
                findings.append(ControlFinding(
                    control_id=cid,
                    name=c["name"],
                    tier=c["tier"],
                    source_lab=c["source_lab"],
                    status="STALE",
                    last_observed=last_time,
                    freshness_seconds=freshness,
                    freshness_slo_seconds=slo,
                    evidence_run_id=evidence.execution.run_id,
                    confidence="provisional",
                    reason=f"Evidence is stale ({freshness}s old, SLO: {slo}s). Re-execution required."
                ))
                continue

            # Evaluate assertions inside evidence
            all_assertions_passed = all(a.passed for a in evidence.assertions) if evidence.assertions else False
            if evidence.result == "passed" and all_assertions_passed:
                status_eval = "PASS"
                reason_eval = f"All {len(evidence.assertions)} assertions verified passed in run {evidence.execution.run_id}."
            elif evidence.result == "degraded":
                status_eval = "DEGRADED"
                reason_eval = f"Evidence indicates degraded performance in run {evidence.execution.run_id}."
            else:
                status_eval = "FAIL"
                failed_assertions = [a.id for a in evidence.assertions if not a.passed]
                reason_eval = f"Assertion failures detected in run {evidence.execution.run_id}: {failed_assertions}"

            findings.append(ControlFinding(
                control_id=cid,
                name=c["name"],
                tier=c["tier"],
                source_lab=c["source_lab"],
                status=status_eval,
                last_observed=last_time,
                freshness_seconds=freshness,
                freshness_slo_seconds=slo,
                evidence_run_id=evidence.execution.run_id,
                confidence="verified",
                reason=reason_eval
            ))

        return findings

    def get_posture(self) -> GovernancePosture:
        """Derives the overall governance posture from individual control evaluations."""
        findings = self.evaluate_controls()
        total = len(findings)
        passing = sum(1 for f in findings if f.status == "PASS")
        failing = sum(1 for f in findings if f.status == "FAIL")
        stale = sum(1 for f in findings if f.status == "STALE")
        unknown = sum(1 for f in findings if f.status == "UNKNOWN")

        if failing > 0:
            overall = "FAIL"
        elif stale > 0 or unknown > 0:
            overall = "DEGRADED"
        else:
            overall = "PASS"

        return GovernancePosture(
            timestamp=datetime.utcnow(),
            overall_status=overall,
            total_controls=total,
            passing_controls=passing,
            failing_controls=failing,
            stale_controls=stale,
            unknown_controls=unknown,
            controls=findings
        )
