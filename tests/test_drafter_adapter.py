from backend.adapters.drafter import DrafterAdapter


def test_metadata_returns_manifest() -> None:
    adapter = DrafterAdapter()
    metadata = adapter.metadata()
    assert metadata["id"] == "drafter"
    assert metadata["status"] == "ready"


def test_health_reports_readiness_field() -> None:
    adapter = DrafterAdapter()
    health = adapter.health()
    assert "ready" in health


def test_run_rejects_empty_message() -> None:
    adapter = DrafterAdapter()
    try:
        adapter.run({"message": "   ", "session_id": None})
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for empty message")
