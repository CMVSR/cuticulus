"""Dataset label utilities."""

import numpy as np
import pandas as pd
from beartype import beartype


@beartype
def labels_to_df(labels: pd.Series) -> pd.DataFrame:
    """Convert label series to dataframe.

    Args:
        labels (pd.Series): Labels to convert.

    Returns:
        pd.DataFrame: Converted labels.
    """
    # convert to dataframe and filter by existing label
    labels = labels.to_frame('class')

    # increment to start index from 1 (images start from 1.jpg)
    labels.index += 1

    return labels


@beartype
def convert_labels(labels: pd.Series) -> pd.DataFrame:
    """Use regex to replace initial string based labels to ints.

    Uses all available classes.

    Args:
        labels (pd.Series): Labels to convert.

    Returns:
        pd.DataFrame: Converted labels as DataFrame.
    """
    labels = labels.replace(
        to_replace='^[r][d].*',
        value=0,
        regex=True,
    ).replace(
        to_replace='^[r][n].*',
        value=1,
        regex=True,
    ).replace(
        to_replace='^[r][r].*',
        value=2,
        regex=True,
    ).replace(
        to_replace='^[r][t].*',
        value=3,
        regex=True,
    )

    # smooth gritty to rough tuberous
    labels = labels.replace(
        to_replace='^[s][g].*',
        value=3,
        regex=True,
    ).replace(
        to_replace='^[s][s].*',
        value=4,
        regex=True,
    )

    # remove the rest
    labels = labels.replace(
        to_replace='^[^0-5].*',
        value=np.nan,
        regex=True,
    ).replace(
        to_replace='[1-3][a,e].*',
        value=np.nan,
        regex=True,
    )

    return labels_to_df(labels)
