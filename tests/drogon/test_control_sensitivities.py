import pytest
from everest.bin.everest_script import everest_entry

def test_control_sensitivities_simulation(capsys):
    """
    Run a basic Drogon control_sensitivities optimization test case.
    """
    try:
        everest_entry(["data/drogon/control_sensitivities/everest/model/controlsens_experiment.yml", "--skip-prompt"])
    except SystemExit as e:
        pytest.fail(f"Everest exited with SystemExit: {e}")

    captured = capsys.readouterr()    
    assert "Everest run finished with" in captured.out
