from pathlib import Path
import os
import subprocess
from ert.resources.forward_models import run_reservoirsimulator


def test_well_trajectory_simulation():
    """
    Run a modified Drogon well_trajectory tutorial test case.

    Modify to run flow sims for first 10 realizations only and
    reduce the max_batch_num to 2 for faster testing.
    """

    # First run flow simulations for the first ten realizations to generate necessary data files
    for realization in range(10):
        path = f"data/drogon/fmu-drogon-flow-files/realization-{realization}/iter-0/eclipse/model"
        original_path = os.getcwd()
        os.chdir(path)
        erun = run_reservoirsimulator.RunReservoirSimulator(
            simulator="flow", version="default", ecl_case=f"DROGON-{realization}.DATA"
        )
        erun.run_flow()
        os.chdir(original_path)

    config_path = Path(
        "data/drogon/well_trajectory/everest/model/welltrajectory_experiment.yml"
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
