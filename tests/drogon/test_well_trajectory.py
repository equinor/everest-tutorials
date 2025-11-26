from pathlib import Path
import pytest
import os
from everest.bin.everest_script import everest_entry
from ert.resources.forward_models import run_reservoirsimulator



def test_well_trajectory_simulation(capsys):
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

    config_path = Path("data/drogon/well_trajectory/everest/model/welltrajectory_experiment.yml")
    config_path.write_text(
        config_path.read_text()
        .replace("max_batch_num: 10", "max_batch_num: 2")
        .replace("realizations: 0-99", "realizations: 0-9")
        .replace("name: lsf", "name: lsf\n    lsf_queue: test")
    )

    well_trajectory_config_path = Path(
        "data/drogon/well_trajectory/everest/input/well_trajectory_config.yml"
    )
    well_trajectory_config_path.write_text(
        well_trajectory_config_path.read_text()
        .replace("  date: 2020-07-01\n", "")
    )
    try:
        everest_entry([str(config_path), "--skip-prompt"])
    except SystemExit as e:
        pytest.fail(f"Everest exited with SystemExit: {e}")

    captured = capsys.readouterr()    
    assert "Everest run finished with" in captured.out
