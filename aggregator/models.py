from typing import List, Dict, Any, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field

ControlStatusType = Literal["PASS", "FAIL", "DEGRADED", "UNKNOWN", "STALE"]

class ExperimentMeta(BaseModel):
    id: str
    name: str

class ExecutionMeta(BaseModel):
    run_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    environment: str = "docker-compose"
    platform: str = "linux-arm64"
    git_sha: Optional[str] = None

class Measurement(BaseModel):
    metric: str
    value: float
    target: Optional[float] = None
    unit: Optional[str] = None
    mode: Literal["measured", "simulated", "emulated", "derived", "assumed"] = "measured"

class Assertion(BaseModel):
    id: str
    name: str
    passed: bool
    detail: Optional[str] = None

class EvidenceRecord(BaseModel):
    schema_version: str = "1.0"
    experiment: ExperimentMeta
    execution: ExecutionMeta
    measurements: List[Measurement] = Field(default_factory=list)
    assertions: List[Assertion] = Field(default_factory=list)
    result: Literal["passed", "failed", "degraded", "unknown"] = "passed"

class ControlFinding(BaseModel):
    control_id: str
    name: str
    tier: str
    source_lab: str
    status: ControlStatusType
    last_observed: Optional[datetime] = None
    freshness_seconds: Optional[int] = None
    freshness_slo_seconds: int = 300
    evidence_run_id: Optional[str] = None
    confidence: Literal["verified", "provisional", "unverified"] = "unverified"
    reason: str

class GovernancePosture(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    overall_status: ControlStatusType
    total_controls: int
    passing_controls: int
    failing_controls: int
    stale_controls: int
    unknown_controls: int
    controls: List[ControlFinding]
