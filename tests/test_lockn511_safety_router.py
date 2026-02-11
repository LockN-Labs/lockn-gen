from tools.safety_router.classifier import RiskClassifier
from tools.safety_router.router_guard import SafetyRouterGuard


classifier = RiskClassifier()
guard = SafetyRouterGuard(classifier)


def test_safe_read():
    result = classifier.classify(tool="read", action="", intent="Read file", payload={"path": "README.md"})
    assert result.risk.value == "safe"


def test_exec_elevated_is_destructive():
    result = classifier.classify(
        tool="exec",
        action="",
        intent="run diag",
        payload={"command": "journalctl -u openclaw", "elevated": True},
    )
    assert result.risk.value == "destructive"
    assert "exec.elevated" in result.triggers


def test_gateway_restart_is_privileged_and_escalates():
    decision = guard.evaluate(
        tool="exec",
        action="gateway restart",
        intent="restart gateway",
        payload={"command": "openclaw gateway restart"},
        local_orchestrator=True,
    )
    assert decision.risk == "privileged"
    assert decision.route == "cloud"
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


def test_destructive_requires_human_approval():
    decision = guard.evaluate(
        tool="exec",
        action="",
        intent="cleanup",
        payload={"command": "rm -rf /tmp/cache"},
        local_orchestrator=True,
    )
    assert decision.route == "cloud"
    assert "human_approval" in decision.approvals
