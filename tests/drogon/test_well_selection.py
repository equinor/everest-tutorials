from pathlib import Path
import subprocess


def test_well_selection_simulation():
    """
    Run a modified Drogon well_selection tutorial test case.
    """

    config_path = Path(
        "data/drogon/well_selection/everest/model/wellselection_experiment.yml"
    )
    config_path.write_text(
        config_path.read_text()
        .replace("max_batch_num: 10", "max_batch_num: 2")
        .replace("realizations: 0-99", "realizations: 0-9")
        .replace("name: lsf\n\n", "name: lsf\n    lsf_queue: test\n\n")
    )

    result = subprocess.run(
        ["everest", "run", str(config_path)],
        capture_output=True,
        text=True,
    )

    assert "EVEREST run finished with" in result.stdout, (
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
