"""
Plotting list of columns for initial and optimal results from EVEREST.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

RESULTS_FILE = (
    "optimization_output/ensembles/batch_{batch}/optimizer/batch_objectives.parquet"
)
PATH_PLOTS = "docs/source/well_order/images/optimization"
FONTSIZE = 15


def read_data(path_results, batches):
    """Get data from optimization"""

    # TODO identify batches
    datas = []
    for batch in batches:
        datas.append(
            pd.read_parquet(
                os.path.join(
                    path_results,
                    RESULTS_FILE.format(
                        batch=batch,
                    ),
                )
            )
        )
    data = pd.concat(datas, ignore_index=True)

    return data


def get_data_improved(data):
    """Identify objective values that improved"""

    OBJECTIVE = "total_objective_value"
    indexes = data.index.to_list()

    best = data.loc[indexes[0], OBJECTIVE]
    improved = [indexes[0]]
    for index in indexes[1:]:
        if data.loc[index, OBJECTIVE] >= best:
            improved.append(index)
            best = data.loc[index, OBJECTIVE]

    return improved


def plot_columns_from_parquet(
    path_results,
    columns,
    batches,
    bounds=(None, None),
    casename="opt",
):
    """Plot columns"""

    os.makedirs(PATH_PLOTS, exist_ok=True)

    results = read_data(path_results, batches)
    indexes = get_data_improved(results)

    plt.figure(figsize=(12, 6))
    # TODO add multi-objective support
    for i, column in enumerate(columns):
        plt.plot(
            results["batch_id"],
            results[column],
            color="dodgerblue",
            zorder=0,
        )
        plt.scatter(
            results["batch_id"],
            results[column],
            marker="o",
            color="salmon",
            s=100,
            edgecolors="black",
        )
        plt.scatter(
            indexes,
            results.loc[indexes, column],
            marker="o",
            color="dodgerblue",
            s=100,
            edgecolors="black",
        )
        increase = results[column].max() - results[column].min()
        plt.text(
            0.95,
            -0.15,
            f"Total objective increase: ${increase:.2e}",
            transform=plt.gca().transAxes,
            fontsize=FONTSIZE,
            fontweight="bold",
            color="black",
            ha="right",
            va="top",
        )

    plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
    plt.ylim(bounds)
    plt.legend(columns, fontsize=FONTSIZE, facecolor="white")
    plt.xlabel("Batch", fontsize=20, fontweight="bold")
    plt.ylabel("Objective functions [$]", fontsize=20, fontweight="bold")
    plt.xticks(fontsize=FONTSIZE)
    plt.yticks(fontsize=FONTSIZE)
    plt.gca().set_axisbelow(True)
    plt.grid(True, color="lightgray", linestyle="dashed")

    # set font size of the exponent
    t = plt.gca().yaxis.get_offset_text()
    t.set_size(FONTSIZE)

    plt.savefig(
        os.path.join(PATH_PLOTS, f"{casename}_objectives.svg"),
        bbox_inches="tight",
    )
    plt.show()


casename = "wo"
path_results = os.path.join(
    "../optimization/drogon/well_order/everest/output/WELLORDER_EXP"
)
columns = ["npv"]
batches = [0, 1, 2, 3, 4, 5]
label = "Batches"

plot_columns_from_parquet(path_results, columns, batches, casename=casename)
