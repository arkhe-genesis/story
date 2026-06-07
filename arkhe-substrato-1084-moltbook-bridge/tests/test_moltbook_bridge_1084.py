import pytest
from datetime import datetime, timezone
from moltbook_bridge_1084 import (
    MoltbookAgentProfile,
    MoltbookAuthAdapter,
    KarmaTheosisConverter,
    ReputationMeshSync,
    AudienceZKBridge,
    CompetitionPuzzleGate,
    MoltbookBridgeOrchestrator
)

def test_karma_converter():
    converter = KarmaTheosisConverter()
    theosis = converter.convert(
        karma=500,
        posts=10,
        comments=20,
        followers=100,
        owner_verified=True
    )
    assert theosis > 0.0
    assert theosis <= 1.0

def test_moltbook_bridge_orchestrator():
    orch = MoltbookBridgeOrchestrator(
        app_key="test_key",
        domain="cathedral-arkhe.org"
    )
    token = "test_token_123"
    result = orch.onboard_agent(token)

    assert result is not None
    assert "agent_id" in result
    assert "theosis" in result
    assert "zk_proof" in result
    assert "merkle_root" in result

    dashboard = orch.get_dashboard()
    assert dashboard["total_onboarded"] == 1
    assert dashboard["mesh"]["nodes"] == 1

def test_competition_puzzle_gate():
    gate = CompetitionPuzzleGate()
    comp_id = "test_comp"

    puzzle_hash = gate.create_puzzle(comp_id, difficulty=0.5)
    assert puzzle_hash is not None

    agent_id = "test_agent"
    theosis = 1.0

    # Needs actual solution hash validation to be fully tested,
    # but basic reject logic works if theosis is low
    result = gate.submit_solution(comp_id, agent_id, "test_solution", 0.1)
    assert result["status"] == "REJECTED"
