import pytest
from everest.bin.everest_script import everest_entry


def test_egg_simulation(capsys):
    """
    Run a basic egg simulation test case.
    """
    try:
        everest_entry(["data/egg/everest/model/egg.yml", "--skip-prompt"])
    except SystemExit as e:
        pytest.fail(f"Everest exited with SystemExit: {e}")

    captured = capsys.readouterr()
    assert "Everest run finished with" in captured.out
