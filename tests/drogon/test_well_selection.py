from pathlib import Path
import pytest
from everest.bin.everest_script import everest_entry


def test_well_selection_simulation(capsys):
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
        .replace("name: lsf", "name: lsf\n    lsf_queue: test")
    )

    try:
        everest_entry([str(config_path), "--skip-prompt"])
    except SystemExit as e:
        pytest.fail(f"Everest exited with SystemExit: {e}")

    captured = capsys.readouterr()
    assert "Everest run finished with" in captured.out
