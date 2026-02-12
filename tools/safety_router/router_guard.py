from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List

from .classifier import RiskClassifier
from .mode import OrchestrationMode, RuntimeModeStore
from .policy import POLICY_MATRIX, RiskTier
from .telemetry import EscalationTelemetry


@dataclass
class GuardDecision:
    risk: str
    mode: str
    guardrails_enabled: bool
    route: str
    selected_model_tier: str
    allowed_on_local: bool
    approvals: List[str]
    triggers: List[str]
    reasons: List[str]
    outcome: str


class SafetyRouterGuard:
    def __init__(
        self,
        classifier: RiskClassifier | None = None,
        mode_store: RuntimeModeStore | None = None,
        telemetry: EscalationTelemetry | None = None,
    ) -> None:
        self.classifier = classifier or RiskClassifier()
        self.mode_store = mode_store or RuntimeModeStore()
        self.telemetry = telemetry

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
        status = self.mode_store.get_status()
        mode = status.mode
        guardrails_enabled = status.guardrails_enabled

        approvals: List[str] = []
        if policy.requires_local_plan:
            approvals.append("local_plan")
        if policy.requires_cloud_approval:
            approvals.append("cloud_approval")
        if policy.requires_human_approval:
            approvals.append("human_approval")

        local_allowed_by_mode = mode in {OrchestrationMode.LOCAL_FIRST, OrchestrationMode.HYBRID}
        cloud_preferred_by_mode = mode == OrchestrationMode.CLOUD_FIRST

        if cloud_preferred_by_mode:
            route = "cloud"
            selected_model_tier = "cloud"
            outcome = "allowed"
        elif local_allowed_by_mode:
            route = "local"
            selected_model_tier = "local-large" if risk_tier == RiskTier.CAUTION else "local-small"
            outcome = "allowed"
        else:
            route = "cloud"
            selected_model_tier = "cloud"
            outcome = "allowed"

        if guardrails_enabled and (not local_orchestrator or not policy.local_execution_allowed or risk_tier in {RiskTier.PRIVILEGED, RiskTier.DESTRUCTIVE}):
            route = "cloud"
            selected_model_tier = "cloud"
            outcome = "escalated"

        decision = GuardDecision(
            risk=risk_tier.value,
            mode=mode.value,
            guardrails_enabled=guardrails_enabled,
            route=route,
            selected_model_tier=selected_model_tier,
            allowed_on_local=policy.local_execution_allowed,
            approvals=approvals,
            triggers=result.triggers,
            reasons=result.reasons,
            outcome=outcome,
        )

        if self.telemetry is not None:
            self.telemetry.log(
                {
                    "event": "lockn511_evaluation",
                    "mode": decision.mode,
                    "guardrails_enabled": decision.guardrails_enabled,
                    "reason": "; ".join(decision.reasons),
                    "trigger": decision.triggers,
                    "selected_model": decision.selected_model_tier,
                    "outcome": decision.outcome,
                    "risk": decision.risk,
                    "tool": tool,
                    "action": action or "",
                }
            )

        return decision

    @staticmethod
    def to_dict(decision: GuardDecision) -> Dict[str, Any]:
        return asdict(decision)
