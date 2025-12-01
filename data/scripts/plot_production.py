import os
import re

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from res2df import summary, ResdataFiles


def numerical_sort(value):
    batch_match = re.search(r"batch_(\d+)", value)
    simulation_match = re.search(r"simulation_(\d+)", value)
    return (
        int(batch_match.group(1)) if batch_match else 0,
        int(simulation_match.group(1)) if simulation_match else 0,
    )


def extract_simulation_number(path):
    match = re.search(r"simulation_(\d+)", path)
    return int(match.group(1)) if match else None


def extract_batch_number(path):
    match = re.search(r"batch_(\d+)", path)
    return int(match.group(1)) if match else None


def find_smspec_files(directory, batch_numberr):
    results = []
    for subdir, dirs, files in os.walk(directory):
        dirs.sort(key=numerical_sort)
        files.sort(key=numerical_sort)
        for filename in files:
            if filename.lower().endswith(".smspec") and "_bak" not in filename.lower():
                filepath = os.path.join(subdir, filename)

                if (
                    extract_simulation_number(filepath) <= number_geo_realizations
                    and extract_batch_number(filepath) == batch_numberr
                ):
                    results.append(filepath)
    return results


def read_summaries(
    simulation_folder,
    batch_numbers,
    keywords_to_be_plotted,
    final_eclipse_simulation_date,
):
    """Read results from flow simulations"""

    data_accumulator = {
        batch: {key: [] for key in keywords_to_be_plotted} for batch in batch_numbers
    }
    all_dates_sets = []

    for batch_number in batch_numbers:
        smspec_files = find_smspec_files(simulation_folder, batch_number)

        filtered_files = [
            f.replace(".SMSPEC", ".DATA")
            for f in smspec_files
            if "_BAK" not in f and f.endswith(".SMSPEC")
        ]

        for file_path in filtered_files:
            # Load data including production rates and dates
            values_npv = summary.df(
                ResdataFiles(file_path),
                column_keys=keywords_to_be_plotted
                + ["DATE", "FOPR", "FGPR", "FWIR", "FWPR"],
            )
            values_npv = values_npv.reset_index()
            values_npv["DATE"] = pd.to_datetime(values_npv["DATE"])
            if final_eclipse_simulation_date not in values_npv["DATE"].values:
                print(
                    "BE CAREFUL, final_eclipse_simulation_date not in values_npv['DATE'].values"
                )
                continue
            all_dates_sets.append(set(values_npv["DATE"]))
            for keyword in keywords_to_be_plotted:
                if keyword in values_npv:  # Check if keyword exists in values_npv
                    data_accumulator[batch_number][keyword].append(
                        values_npv[["DATE", keyword]]
                    )

    # Determine common dates across all files and batches
    common_dates = set.intersection(*all_dates_sets) if all_dates_sets else set()

    return data_accumulator, common_dates


def plot_summaries(
    data_accumulator,
    batch_numbers,
    common_dates,
    keywords_to_be_plotted,
    time_period,
    plots_folder,
    casename="opt",
):
    """Plot summary values"""

    plt.rcParams["text.usetex"] = False
    plt.rcParams["font.family"] = "DejaVu Sans"
    sns.set_theme(style="darkgrid")
    sns.set_context("paper")

    os.makedirs(plots_folder, exist_ok=True)

    percentile = 0.1

    color_start = 0.5  # Start from 30% into the colormap to avoid very light colors

    batch_colors = [plt.cm.Blues(color_start), "red"]
    batch_colors = ["#00B7EB", "#FFFF00"]
    batch_colors = ["#58508d", "#ffa600"]

    for keyword in keywords_to_be_plotted:
        print(f"Plotting: {keyword}")

        _, ax = plt.subplots(figsize=(16, 9))
        max_means = []

        for batch_index, batch in enumerate(batch_numbers):
            if data_accumulator[batch][keyword]:
                # Concatenate and filter the data
                combined_data = pd.concat(
                    data_accumulator[batch][keyword], ignore_index=True
                )
                combined_data = combined_data[combined_data["DATE"].isin(common_dates)]

                if not combined_data.empty:
                    combined_data.set_index("DATE", inplace=True)
                    combined_data.sort_index(inplace=True)

                    mean_curve = combined_data.groupby(level=0)[keyword].mean()
                    mean_90_curve = combined_data.groupby(level=0)[keyword].quantile(
                        1 - percentile
                    )
                    mean_10_curve = combined_data.groupby(level=0)[keyword].quantile(
                        percentile
                    )
                    max_mean_curve = max(mean_curve)
                    max_means.append((batch_index, max_mean_curve))
                    if keyword.startswith(("FWIT", "WWIR")):
                        line_color = (
                            "#58508d"
                            if batch_index < len(batch_numbers) - 1
                            else "#ffa600"
                        )
                        linewidth_value = 10
                        ax.plot(
                            mean_curve.index,
                            mean_curve,
                            color=line_color,
                            linewidth=4,
                            label="Mean" if batch_index == 9999 else "",
                        )
                    # Plotting statistical lines
                    else:
                        line_color = (
                            "black" if batch_index < len(batch_numbers) - 1 else "grey"
                        )
                        linewidth_value = 2

                        ax.plot(
                            mean_curve.index,
                            mean_curve,
                            color=line_color,
                            linewidth=4,
                            label="Mean" if batch_index == 0 else "",
                        )
                        ax.plot(
                            mean_90_curve.index,
                            mean_90_curve,
                            color=line_color,
                            linestyle="--",
                            linewidth=linewidth_value,
                            label="P10 Percentile" if batch_index == 0 else "",
                        )
                        ax.plot(
                            mean_10_curve.index,
                            mean_10_curve,
                            color=line_color,
                            linestyle=":",
                            linewidth=linewidth_value,
                            label="P90 Percentile" if batch_index == 0 else "",
                        )

                    label = f"Batch {batch}"
                    ax.fill_between(
                        mean_curve.index,
                        mean_10_curve,
                        mean_90_curve,
                        color=batch_colors[batch_index],
                        alpha=0.7,
                        label=label,
                    )

        if len(batch_numbers) != 1:
            ## if error, most prob. eclipse keyword or date not present in eclipse output
            try:
                if max_means[0][1] == 0:
                    continue
            except IndexError:
                print(
                    "Plot will remain blank. Most probably, KEYWORD or DATE not present"
                )

        ax.set_title(f"{keyword}", fontsize=24, fontweight="bold")
        ax.set_xlabel("Date", fontsize=26, fontweight="bold")
        ax.set_ylabel(
            (
                f"{keyword} [Sm³/day]"
                if keyword in ["FOPR", "FWPR", "FGPR", "FWIR"]
                else (
                    f"{keyword} [Sm³]"
                    if keyword in ["FOPT", "FWPT", "FGPT", "FWIT"]
                    else (
                        f"{keyword} [Sm³/day]"
                        if keyword.startswith(("WOPR", "WWIR", "WWPR", "WGPR"))
                        else (
                            "Recovery factor"
                            if keyword == "FOE"
                            else (
                                "Net Present Value [$]"
                                if keyword == "NPV"
                                else (
                                    "FPR [Bar]" if keyword in ["FPR"] else f"{keyword}"
                                )
                            )
                        )
                    )
                )
            ),
            fontsize=24,
            fontweight="bold",
        )

        ax.yaxis.get_offset_text().set_fontsize(24)
        ax.legend(fontsize=22)

        plt.xticks(rotation=0, fontsize=24)
        plt.yticks(rotation=0, fontsize=24)
        plt.xlim((time_period[0] - 1970) * 365, (time_period[1] - 1970) * 365 + 31)
        plt.tight_layout()

        plt.savefig(
            os.path.join(plots_folder, f"{casename}_{keyword.replace(':', '_')}.svg"),
            bbox_inches="tight",
        )
        plt.close()


casename = "wo"
simulation_folder = (
    "../optimization/drogon/well_order/everest/output/WELLORDER_EXP/simulation_output/"
)
plots_folder = "docs/source/well_order/images/production/"

keywords_to_be_plotted = [
    "FOPR",
    "FWPR",
    "FGPR",
    "FOPT",
    "FWPT",
    "FGPT",
    "FWIR",
    "FWIT",
    "FPR",
    "WOPR:A1",
    "WOPR:A2",
    "WOPR:A3",
    "WOPR:A4",
    "WGPR:A1",
    "WGPR:A2",
    "WGPR:A3",
    "WGPR:A4",
    "WWPR:A1",
    "WWPR:A2",
    "WWPR:A3",
    "WWPR:A4",
    "WWIR:A5",
    "WWIR:A6",
]

final_eclipse_simulation_date = pd.to_datetime("2030-01-01 00:00:00")
batch_numbers = [0, 5]
number_geo_realizations = 99  # this is simulation index of last realization
time_period = [2023, 2030]

data_accumulator, common_dates = read_summaries(
    simulation_folder,
    batch_numbers,
    keywords_to_be_plotted,
    final_eclipse_simulation_date,
)

plot_summaries(
    data_accumulator,
    batch_numbers,
    common_dates,
    keywords_to_be_plotted,
    time_period,
    plots_folder,
    casename=casename,
)
