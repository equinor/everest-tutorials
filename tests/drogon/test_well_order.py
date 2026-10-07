import subprocess
from pathlib import Path


def test_well_order_simulation():
    """
    Run a modified Drogon well_order tutorial test case.
    """

    config_path = Path("data/drogon/well_order/everest/model/wellorder_experiment.yml")
    config_path.write_text(
        config_path.read_text()
        .replace("max_batch_num: 10", "max_batch_num: 2")
        .replace("realizations: r{{range(100) | list()}}", "realizations: 0-9")
        .replace("name: lsf", "name: lsf\n    lsf_queue: test")
    )

    result = subprocess.run(
        ["everest", "run", str(config_path)],
        capture_output=True,
        text=True,
    )

    assert "EVEREST run finished with" in result.stdout, (
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
