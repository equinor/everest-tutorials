import os
from pathlib import Path
import shutil
from typing import Tuple
from packaging.version import parse as parse_version
from ert.run_models.everest_run_model import EverestRunModel
from everest.config import EverestConfig
from ert.ensemble_evaluator import EvaluatorServerConfig
from ert.shared import __version__ as ert_version
from everest.api import EverestDataAPI
import polars as pl
import io


def setup_environment(snapshot, source_root: Path, experiment_name: str, config_file: str) -> Tuple[EverestConfig, str]:
    reference_path = source_root / snapshot.snapshot_dir
    references = [f.stem for f in reference_path.glob("*.csv")]
    release_name = parse_version(ert_version)
    filtered_sorted_references = sorted(
        ref for ref in references if parse_version(ref) <= release_name
    )
    if filtered_sorted_references:
        reference = filtered_sorted_references[-1]
    else:
        raise ValueError(
            f"There is no reference snapshot for or before release {release_name}"
        )
    reference_file = f"{reference}.csv"

    os.chdir(source_root / "data" / "drogon" / experiment_name / "everest" / "model")
    config = EverestConfig.load_file(config_file)
    config.optimization.speculative = True
    config.optimization.max_batch_num = 2
    config.model.realizations = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    config.model.realizations_weights = [1 / len(config.model.realizations)] * len(config.model.realizations)

    # Dump and read modified config file:
    modified_config_file = f"{Path(config_file).stem}_modified.yml"
    config.dump(modified_config_file)
    modified_config = EverestConfig.load_file(modified_config_file)
    return (modified_config, reference_file)

def run_and_assert_experiment(snapshot, snapshot_reference: str, config: EverestConfig) -> None:
    parsed_ert_version = parse_version(ert_version)

    run_model = EverestRunModel.create(config)
    evaluator_server_config = EvaluatorServerConfig()
    run_model.run_experiment(evaluator_server_config)

    if parsed_ert_version >= parse_version("14.0.0b0"):
        experiment_results_csv = _read_opt_and_summary_data(config, parsed_ert_version)
        snapshot.assert_match(experiment_results_csv, snapshot_reference)
    else:
        # New storage solution doesn't exist, use old export functionality
        from everest.export import export_data
        data = export_data(
            export_config=config.export,
            output_dir=config.output_dir,
            data_file=config.model.data_file if config.model else None,
        )
        snapshot.assert_match(data.drop(columns=["start_time", "end_time"], axis=1).round(6).to_csv(), snapshot_reference)

def cleanup(request) -> None:
    if not request.config.getoption("--skip-cleanup"):
        if hasattr(request.node, 'rep_call') and request.node.rep_call.passed:
                # Only remove simulation results when test passes in
                # order to inspect failed test results
                shutil.rmtree(os.path.join("..", "output"), ignore_errors=True)

def _read_opt_and_summary_data(ever_config: EverestConfig, parsed_ert_version: str) -> str:
    api = EverestDataAPI(ever_config)
    summary_data_df = api.summary_values()
    columns_to_drop = [col for col in ["TCPU", "TCPUDAY"] if col in summary_data_df.columns]
    summary_data_df = summary_data_df.drop(columns_to_drop)
    if parsed_ert_version >= parse_version("14.2.1b0"):
        from everest.everest_storage import EverestStorage
        ever_storage = EverestStorage(output_dir=Path(ever_config.optimization_output_dir))
        ever_storage.init(
            formatted_control_names=ever_config.formatted_control_names,
            objective_functions=ever_config.objective_functions,
            output_constraints=ever_config.output_constraints,
            realizations=ever_config.model.realizations,
        )
        ever_storage.read_from_output_dir()
        opt_df, _, _ = ever_storage.export_dataframes()
    else:
        opt_df, _, _ = api.export_dataframes()

    # Sort summary dataframe in same way as the older dataframe
    sort_sum_data_df = summary_data_df.sort(["batch", "date", "simulation"])

    # Filter out perturbation (old dataframe only contains function evaluations) and drop unnecessary columns
    filtered_opt_df = opt_df.filter(~((opt_df["perturbation"].is_not_null()) & (opt_df["simulation_id"].is_null())))
    short_filt_opt_df = filtered_opt_df.drop(["perturbation", "simulation_id"])

    # Repeat batches for each reporting step
    short_filt_opt_df = short_filt_opt_df.rename({"batch_id": "batch"})
    experiment_results = sort_sum_data_df.join(short_filt_opt_df, on=["batch", "realization"], how="inner")
    return _extract_csv_from_df(experiment_results)

def _extract_csv_from_df(df: pl.DataFrame) -> str:
    csv_buffer = io.StringIO()
    df.write_csv(csv_buffer)
    return csv_buffer.getvalue()
