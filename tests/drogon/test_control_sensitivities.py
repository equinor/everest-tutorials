import subprocess
from pathlib import Path


def test_control_sensitivities_simulation():
    """
    Run a modified Drogon control_sensitivities tutorial test case.
    """

    config_path = Path(
        "data/drogon/control_sensitivities/everest/model/controlsens_experiment.yml"
    )
    config_path.write_text(
        config_path.read_text()
        .replace("realizations: 0-99", "realizations: 0-9")
        .replace("name: lsf", "name: lsf\n\n    lsf_queue: test\n")
    )

    result = subprocess.run(
        ["everest", "run", str(config_path)],
        capture_output=True,
        text=True,
    )

    assert "EVEREST run finished with" in result.stdout, (
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
