import json

from tools.safety_router.classifier import RiskClassifier
from tools.safety_router.mode import RuntimeModeStore
from tools.safety_router.router_guard import SafetyRouterGuard
from tools.safety_router.telemetry import EscalationTelemetry


classifier = RiskClassifier()


def _guard(tmp_path, mode: str = "hybrid", enabled: bool = True) -> SafetyRouterGuard:
    mode_store = RuntimeModeStore(tmp_path / "mode.json")
    mode_store.set_mode(mode, actor="test")
    mode_store.set_guardrails_enabled(enabled, actor="test")
    telemetry = EscalationTelemetry(tmp_path / "telemetry.jsonl")
    return SafetyRouterGuard(classifier=classifier, mode_store=mode_store, telemetry=telemetry)


def test_safe_read(tmp_path):
    guard = _guard(tmp_path)
    result = classifier.classify(tool="read", action="", intent="Read file", payload={"path": "README.md"})
    assert result.risk.value == "safe"

    decision = guard.evaluate(tool="read", action="", intent="Read file", payload={"path": "README.md"})
    assert decision.mode == "hybrid"


def test_exec_elevated_is_destructive():
    result = classifier.classify(
        tool="exec",
        action="",
        intent="run diag",
        payload={"command": "journalctl -u openclaw", "elevated": True},
    )
    assert result.risk.value == "destructive"
    assert "exec.elevated" in result.triggers


def test_gateway_restart_is_privileged_and_escalates(tmp_path):
    guard = _guard(tmp_path)
    decision = guard.evaluate(
        tool="exec",
        action="gateway restart",
        intent="restart gateway",
        payload={"command": "openclaw gateway restart"},
        local_orchestrator=True,
    )
    assert decision.risk == "privileged"
    assert decision.route == "cloud"
    assert "local_plan" in decision.approvals
    assert "cloud_approval" in decision.approvals


def test_gateway_command_is_privileged():
    result = classifier.classify(
        tool="exec",
        action="",
        intent="restart infra",
        payload={"command": "openclaw gateway restart"},
    )
    assert result.risk.value == "privileged"


def test_prod_keyword_is_privileged():
    result = classifier.classify(
        tool="exec",
        action="",
        intent="Deploy prod auth fix",
        payload={"command": "./deploy.sh --env prod"},
    )
    assert result.risk.value == "privileged"


def test_destructive_pattern_detected():
    result = classifier.classify(
        tool="exec",
        action="",
        intent="cleanup",
        payload={"command": "rm -rf /tmp/cache"},
    )
    assert result.risk.value == "destructive"


def test_destructive_requires_human_approval(tmp_path):
    guard = _guard(tmp_path)
    decision = guard.evaluate(
        tool="exec",
        action="",
        intent="cleanup",
        payload={"command": "rm -rf /tmp/cache"},
        local_orchestrator=True,
    )
    assert decision.route == "cloud"
    assert "human_approval" in decision.approvals


def test_cloud_first_mode_routes_safe_to_cloud(tmp_path):
    guard = _guard(tmp_path, mode="cloud-first")
    decision = guard.evaluate(
        tool="read",
        action="",
        intent="Read file",
        payload={"path": "README.md"},
    )
    assert decision.mode == "cloud-first"
    assert decision.route == "cloud"


def test_guardrails_disabled_keeps_legacy_route(tmp_path):
    guard = _guard(tmp_path, mode="local-first", enabled=False)
    decision = guard.evaluate(
        tool="exec",
        action="gateway restart",
        intent="restart gateway",
        payload={"command": "openclaw gateway restart"},
        local_orchestrator=True,
    )
    assert decision.guardrails_enabled is False
    assert decision.route == "local"
    assert decision.outcome == "allowed"


def test_telemetry_written(tmp_path):
    guard = _guard(tmp_path)
    _ = guard.evaluate(
        tool="exec",
        action="",
        intent="cleanup",
        payload={"command": "rm -rf /tmp/cache"},
        local_orchestrator=True,
    )
    telemetry_path = tmp_path / "telemetry.jsonl"
    lines = telemetry_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert payload["event"] == "lockn511_evaluation"
    assert payload["risk"] == "destructive"
