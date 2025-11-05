import pytest
from tests.helper_methods import cleanup, run_and_assert_experiment, setup_environment


@pytest.mark.timeout(60 * 120)
def test_drogon_well_rate_short(request, source_root):
    """
    Run shortened Drogon case (max 2 batches, 10 realizations) for optimizing
    production and injection rates of individual wells.
    """
    try:
        config = setup_environment(
            source_root,
            experiment_name="well_rate",
            config_file="wellrate_experiment.yml",
        )
        run_and_assert_experiment(config)
    finally:
        cleanup(request)
