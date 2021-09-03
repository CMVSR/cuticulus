
import os
import logging

import numpy as np
import pandas as pd

# for debugging, env logging level must be set to debug/info
from cuticle_analysis.core import init
init()

logger = logging.getLogger(__name__)

size_col = "Size"
samples_col = "Samples (per class)"
acc_col = "Accuracy (avg)"
loss_col = "Loss (avg)"


def experiment_1() -> pd.DataFrame:
    """
        Analyze the results of experiment 1.
    """
    filepath = "./output/experiment_1.csv"
    if not os.path.isfile(filepath):
        logger.info(
            "Error: experiment_1.csv does not exist. Skipping analysis.")
        return

    df = pd.read_csv(filepath)
    sizes = np.sort(df["size"].unique())
    samples_per_class = np.sort(df["samples_per_class"].unique())

    res_cols = [size_col, samples_col, acc_col, loss_col]
    res_df = pd.DataFrame(columns=res_cols)
    for size in sizes:
        for samples in samples_per_class:
            temp = df[(df["size"] == size) & (
                df["samples_per_class"] == samples)]
            res_df = res_df.append(
                {
                    size_col: f"({int(size)}, {int(size)})",
                    samples_col: samples,
                    acc_col: round(temp["test_accuracy"].mean(), 3)*100,
                    loss_col: round(temp["test_loss"].mean(), 3)
                }, ignore_index=True)

    return res_df


if __name__ == "__main__":
    e1_res = experiment_1()
    logger.info(e1_res)

    # save to latex file
    e1_res.to_latex("./paper/tables/experiment_1.tex", index=False)
