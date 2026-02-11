from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List

from .policy import RiskTier


PROD_AUTH_BILLING_SECURITY = re.compile(
    r"\b(prod|production|auth|authentication|billing|payment|security|secret|token|credential)\b",
    re.IGNORECASE,
)

DESTRUCTIVE_SHELL_PATTERNS = [
    r"\brm\s+-rf\b",
    r"\bdd\s+if=",
    r"\bmkfs\b",
    r"\bshutdown\b",
    r"\breboot\b",
    r":\(\)\s*\{\s*:\|:\s*&\s*\};:\s*",
    r"\bterraform\s+destroy\b",
    r"\bkubectl\s+delete\b",
    r"\bdrop\s+database\b",
    r"\btruncate\s+table\b",
]

GATEWAY_SENSITIVE_ACTIONS = {
    "gateway config",
    "gateway update",
    "gateway restart",
    "gateway stop",
}


@dataclass
class ClassificationResult:
    risk: RiskTier
    triggers: List[str] = field(default_factory=list)
    reasons: List[str] = field(default_factory=list)


class RiskClassifier:
    """Classify risk for tool+action+intent payloads."""

    def classify(
        self,
        *,
        tool: str,
        action: str | None = None,
        intent: str | None = None,
        payload: Dict[str, Any] | None = None,
    ) -> ClassificationResult:
        payload = payload or {}
        intent_text = (intent or "").strip()
        action_text = (action or "").strip().lower()

        triggers: List[str] = []
        reasons: List[str] = []

        if tool == "exec" and bool(payload.get("elevated")):
            triggers.append("exec.elevated")
            reasons.append("Elevated shell execution requested")
            return ClassificationResult(RiskTier.DESTRUCTIVE, triggers, reasons)

        if action_text and action_text in GATEWAY_SENSITIVE_ACTIONS:
            triggers.append(f"gateway.action:{action_text}")
            reasons.append("Gateway configuration/update lifecycle action")

        command = str(payload.get("command", ""))

        gateway_command_patterns = [
            r"\bopenclaw\s+gateway\s+config\b",
            r"\bopenclaw\s+gateway\s+update\b",
            r"\bopenclaw\s+gateway\s+restart\b",
            r"\bopenclaw\s+gateway\s+stop\b",
        ]
        for gp in gateway_command_patterns:
            if re.search(gp, command, flags=re.IGNORECASE):
                triggers.append(f"gateway.command:{gp}")
                reasons.append("Gateway lifecycle command detected")
                break

        for pattern in DESTRUCTIVE_SHELL_PATTERNS:
            if re.search(pattern, command, flags=re.IGNORECASE):
                triggers.append(f"destructive_pattern:{pattern}")
                reasons.append("Potentially destructive shell command pattern")
                return ClassificationResult(RiskTier.DESTRUCTIVE, triggers, reasons)

        text_blob = " ".join(x for x in [intent_text, command, action_text] if x)
        if PROD_AUTH_BILLING_SECURITY.search(text_blob):
            triggers.append("sensitive_keyword")
            reasons.append("Intent includes prod/auth/billing/security sensitive scope")

        if any(t.startswith("gateway.action:") or t.startswith("gateway.command:") for t in triggers):
            return ClassificationResult(RiskTier.PRIVILEGED, triggers, reasons)

        if "sensitive_keyword" in triggers:
            return ClassificationResult(RiskTier.PRIVILEGED, triggers, reasons)

        if tool in {"linear_update_issue", "linear_create_issue", "notion_API-patch-page"}:
            return ClassificationResult(RiskTier.CAUTION, ["tool.write"], ["External system write operation"])

        return ClassificationResult(RiskTier.SAFE, triggers, reasons or ["No sensitive triggers matched"])
