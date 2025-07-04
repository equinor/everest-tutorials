"""
Plotting list of columns for initial and optimal results from EVEREST.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


RESULTS_FILE = (
    "optimization_output/ensembles/batch_{batch}/"
    "optimizer/realization_controls.parquet"
)
PATH_PLOTS = "docs/source/well_order/images/optimization"
FONTSIZE = 15


def read_data_for_batches(path_results, batches):
    """Get data for initial and optimal batch"""

    if len(batches) > 2:
        raise Exception("Plotting of only 2 batches supported.")

    data_initial = pd.read_parquet(
        os.path.join(
            path_results,
            RESULTS_FILE.format(batch=batches[0]),
        )
    )
    data_optimal = pd.read_parquet(
        os.path.join(
            path_results,
            RESULTS_FILE.format(batch=batches[-1]),
        )
    )

    # take only first realization
    data_initial = data_initial[columns].iloc[0, :]
    data_optimal = data_optimal[columns].iloc[0, :]

    return data_initial, data_optimal


def plot_columns_from_parquet(
    path_results,
    batches,
    columns,
    bounds,
    label,
    casename="opt",
):
    """Plot columns for initial and optimal batch"""

    os.makedirs(PATH_PLOTS, exist_ok=True)

    results_initial, results_optimal = read_data_for_batches(
        path_results,
        batches,
    )

    plt.figure(figsize=(12, 6))
    plt.scatter(
        columns,
        results_initial,
        marker="o",
        color="gold",
        s=100,
        edgecolors="black",
    )
    plt.scatter(
        columns,
        results_optimal,
        marker="o",
        color="dodgerblue",
        s=100,
        edgecolors="black",
    )

    plt.ylim(bounds)
    plt.legend(
        ["Initial", "Optimized"],
        fontsize=FONTSIZE,
        facecolor="white",
    )
    plt.xlabel(
        label,
        fontsize=20,
        fontweight="bold",
    )
    plt.ylabel(
        "Value",
        fontsize=20,
        fontweight="bold",
    )
    plt.xticks(rotation=45, fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.gca().set_axisbelow(True)
    plt.grid(
        True,
        color="lightgray",
        linestyle="dashed",
    )

    plt.savefig(
        os.path.join(PATH_PLOTS, f"{casename}_controls.svg"),
        bbox_inches="tight",
    )
    plt.close()


casename = "wo"
path_results = os.path.join(
    "../optimization/drogon/well_order/everest/output/WELLORDER_EXP2"
)
columns = [
    "well_order.A1",
    "well_order.A2",
    "well_order.A3",
    "well_order.A4",
    "well_order.A5",
    "well_order.A6",
]
batches = [0, 5]
bounds = [0, 1]
label = "Optimization Variables"

plot_columns_from_parquet(
    path_results,
    batches,
    columns,
    bounds,
    label,
    casename=casename,
)
