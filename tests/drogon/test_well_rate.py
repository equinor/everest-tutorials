import pytest
from pathlib import Path
from everest.bin.everest_script import everest_entry


def test_well_rate_simulation(capsys):
    """
    Run a modified Drogon well_rate tutorial test case.
    """

    config_path = Path("data/drogon/well_rate/everest/model/wellrate_experiment.yml")
    config_path.write_text(
        config_path.read_text()
        .replace("max_batch_num: 10", "max_batch_num: 2")
        .replace("realizations: r{{range(100) | list()}}", "realizations: 0-9")
        .replace("name: lsf", "name: lsf\n    lsf_queue: test")
    )
    try:
        everest_entry([str(config_path), "--skip-prompt"])
    except SystemExit as e:
        pytest.fail(f"Everest exited with SystemExit: {e}")

    captured = capsys.readouterr()
    assert "Everest run finished with" in captured.out
