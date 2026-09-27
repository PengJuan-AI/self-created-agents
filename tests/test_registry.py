from tools.validate_agents import validate


def test_registry_and_manifests_are_valid() -> None:
    errors = validate()
    assert errors == []
