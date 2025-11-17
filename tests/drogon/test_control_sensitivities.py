import pytest
from everest.bin.everest_script import everest_entry
from pathlib import Path

def test_control_sensitivities_simulation(capsys):
    """
    Run a modified Drogon control_sensitivities tutorial test case.
    """

    config_path = Path("data/drogon/control_sensitivities/everest/model/controlsens_experiment.yml")
    config_path.write_text(
        config_path.read_text()
        .replace("realizations: 0-99", "realizations: 0-9")
        .replace("name: lsf", "name: lsf\n    lsf_queue: test")
    )

    try:
        everest_entry([str(config_path), "--skip-prompt"])
    except SystemExit as e:
        pytest.fail(f"Everest exited with SystemExit: {e}")

    captured = capsys.readouterr()    
    assert "Everest run finished with" in captured.out
