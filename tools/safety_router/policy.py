from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List


class RiskTier(str, Enum):
    SAFE = "safe"
    CAUTION = "caution"
    PRIVILEGED = "privileged"
    DESTRUCTIVE = "destructive"


@dataclass(frozen=True)
class PolicyRule:
    risk: RiskTier
    allowed_model_tiers: List[str]
    requires_cloud_approval: bool
    requires_human_approval: bool
    local_execution_allowed: bool


POLICY_MATRIX: Dict[RiskTier, PolicyRule] = {
    RiskTier.SAFE: PolicyRule(
        risk=RiskTier.SAFE,
        allowed_model_tiers=["local-small", "local-large", "cloud"],
        requires_cloud_approval=False,
        requires_human_approval=False,
        local_execution_allowed=True,
    ),
    RiskTier.CAUTION: PolicyRule(
        risk=RiskTier.CAUTION,
        allowed_model_tiers=["local-large", "cloud"],
        requires_cloud_approval=False,
        requires_human_approval=False,
        local_execution_allowed=True,
    ),
    RiskTier.PRIVILEGED: PolicyRule(
        risk=RiskTier.PRIVILEGED,
        allowed_model_tiers=["cloud"],
        requires_cloud_approval=True,
        requires_human_approval=False,
        local_execution_allowed=False,
    ),
    RiskTier.DESTRUCTIVE: PolicyRule(
        risk=RiskTier.DESTRUCTIVE,
        allowed_model_tiers=["cloud"],
        requires_cloud_approval=True,
        requires_human_approval=True,
        local_execution_allowed=False,
    ),
}


def policy_matrix_as_dict() -> Dict[str, dict]:
    return {tier.value: asdict(rule) for tier, rule in POLICY_MATRIX.items()}
