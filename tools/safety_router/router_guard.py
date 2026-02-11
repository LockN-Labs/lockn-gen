from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List

from .classifier import RiskClassifier
from .policy import POLICY_MATRIX, RiskTier


@dataclass
class GuardDecision:
    risk: str
    route: str
    selected_model_tier: str
    allowed_on_local: bool
    approvals: List[str]
    triggers: List[str]
    reasons: List[str]
    outcome: str


class SafetyRouterGuard:
    def __init__(self, classifier: RiskClassifier | None = None) -> None:
        self.classifier = classifier or RiskClassifier()

    def evaluate(
        self,
        *,
        tool: str,
        action: str | None,
        intent: str | None,
        payload: Dict[str, Any] | None,
        local_orchestrator: bool = True,
    ) -> GuardDecision:
        result = self.classifier.classify(tool=tool, action=action, intent=intent, payload=payload)
        risk_tier = result.risk
        policy = POLICY_MATRIX[risk_tier]

        approvals: List[str] = []
        if policy.requires_cloud_approval:
            approvals.append("cloud_approval")
        if policy.requires_human_approval:
            approvals.append("human_approval")

        if local_orchestrator and not policy.local_execution_allowed:
            route = "cloud"
            selected_model_tier = "cloud"
            outcome = "escalated"
        else:
            route = "local"
            selected_model_tier = "local-large" if risk_tier == RiskTier.CAUTION else "local-small"
            outcome = "allowed"

        if risk_tier in {RiskTier.PRIVILEGED, RiskTier.DESTRUCTIVE} and local_orchestrator:
            outcome = "escalated"

        return GuardDecision(
            risk=risk_tier.value,
            route=route,
            selected_model_tier=selected_model_tier,
            allowed_on_local=policy.local_execution_allowed,
            approvals=approvals,
            triggers=result.triggers,
            reasons=result.reasons,
            outcome=outcome,
        )

    @staticmethod
    def to_dict(decision: GuardDecision) -> Dict[str, Any]:
        return asdict(decision)
