from pathlib import Path
import pytest
from everest.bin.everest_script import everest_entry

def test_well_swap_simulation(capsys):
    """
    Run a basic Drogon well_swap optimization test case.
    """

    config_path = Path("data/drogon/well_swap/everest/model/wellswap_experiment.yml")
    config_path.write_text(config_path.read_text().replace('max_batch_num: 10', 'max_batch_num: 2'))

    try:
        everest_entry([str(config_path), "--skip-prompt"])
    except SystemExit as e:
        pytest.fail(f"Everest exited with SystemExit: {e}")

    captured = capsys.readouterr()    
    assert "Everest run finished with" in captured.out
