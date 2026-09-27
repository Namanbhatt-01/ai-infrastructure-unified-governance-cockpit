from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

class TelemetryEvent(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tier: str = Field(..., description="Source architectural tier: tier1_fabric, tier2_netdevops, tier3_assurance, tier4_secops, tier5_rag")
    metric_name: str
    value: float
    labels: Dict[str, str] = Field(default_factory=dict)
    event_metadata: Optional[Dict[str, Any]] = None

class CockpitSummary(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    fabric_status: str
    active_threats: int
    cross_tenant_leaks: int
    p99_inference_latency_ms: float
    slo_availability_percent: float
    compliance_score_percent: float
    tier_health: Dict[str, str]
