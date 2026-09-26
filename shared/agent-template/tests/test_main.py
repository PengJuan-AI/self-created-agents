from src.main import run


def test_run_returns_a_response() -> None:
    assert "Agent received" in run("hello")
