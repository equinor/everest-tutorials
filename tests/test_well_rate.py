import pytest
from tests.helper_methods import cleanup, run_and_assert_experiment, setup_environment


@pytest.mark.timeout(60 * 120)
def test_drogon_well_rate_short(request, snapshot, source_root):
    """
    Run shortened Drogon case (max 2 batches, 10 realizations) for optimizing production and injection rates of individual wells
    and assert that the result compares with the most recent reference case for this release and flow version.
    """
    try:
        config, snapshot_reference = setup_environment(
            snapshot, 
            source_root, 
            experiment_name="well_rate", 
            config_file="wellrate_experiment.yml"
        )
        run_and_assert_experiment(snapshot, snapshot_reference, config)
    finally:
        cleanup(request)
