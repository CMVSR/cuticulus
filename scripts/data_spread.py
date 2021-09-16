
from typing import Dict, List
import logging

import pandas as pd

# for debugging, env logging level must be set to debug/info
from cuticle_analysis.core import init
init()

from cuticle_analysis import const  # noqa
from cuticle_analysis.datasets import Dataset  # noqa
from cuticle_analysis.datasets import AllFull  # noqa
from cuticle_analysis.datasets import RoughSmoothFull  # noqa
from cuticle_analysis.datasets import RoughSmoothSub  # noqa


logger = logging.getLogger(__name__)

all_labels = list(const.ALL_LABEL_MAP.keys())
all_labels.remove('_background_')
rs_labels = list(const.RS_LABEL_MAP.keys())
rs_labels.remove('_background_')

_TOTAL = 'Total'
_TYPE = 'Type'


def total_samples(class_data: Dict) -> int:
    """
        Total number of samples in the dataset.

        Args:
            class_data: Dictionary of class labels and number of samples.

        Returns:
            total: Total number of samples per class label.
    """
    res = 0
    for _, data in class_data.items():
        res += data
    return res


def append_all(df: pd.DataFrame, data: Dataset, cols: List, _type: str) -> pd.DataFrame:
    """
        Build a all class distribution row from an input dataset and append the
        row to a dataframe.
    """
    def all_row(type: str, class_data: Dict, _cols: List) -> pd.DataFrame:
        """
            Build a row for the all class distribution table.
        """
        data = [class_data[label] for label in all_labels]
        cols = [type] + data + [total_samples(class_data)]
        row = pd.DataFrame(
            [cols], columns=_cols)
        return row

    row = all_row(_type, data.class_data(), cols)
    df = df.append(row, ignore_index=True)

    return df


def append_rs(df: pd.DataFrame, data: Dataset, cols: List, _type: str) -> pd.DataFrame:
    """
        Build a rough smooth class distribution row from an input dataset and
        append the row to a dataframe.
    """
    def rs_row(type: str, size: tuple, class_data: Dict, _cols: List) -> pd.DataFrame:
        """
            Build a row for the rough smooth class distribution table.
        """
        if type != 'full':
            type = f'{size}'

        data = [class_data[label] for label in rs_labels]
        cols = [type] + data + [total_samples(class_data)]
        row = pd.DataFrame([cols], columns=_cols)
        return row

    row = rs_row(_type, data.size, data.class_data(), cols)
    df = df.append(row, ignore_index=True)

    return df


def distribution_pct(df: pd.DataFrame, cols: List) -> pd.DataFrame:
    """
    Calculate the distribution of a class in a dataframe as a percent.
    Returns:
        df: Transposed dataframe with the columns ['Label', 'Samples (n)', 'Samples (%)']
    """
    sample_pct = df.loc[:, cols[1:]].div(
        df[_TOTAL], axis=0).astype(float).round(2)
    df = df.append(sample_pct, ignore_index=True)
    df = df.transpose().rename(
        columns={_TYPE: 'Label', 0: 'Samples (n)', 1: 'Samples (%)'})
    df.rename_axis('Label', axis=1, inplace=True)
    return df


def all_full_df(cols: List) -> pd.DataFrame:
    """
        Create all full dataset class distribution table. Add percent samples
        column.
    """
    # init output tables
    df = pd.DataFrame(columns=cols)

    # add all full dataset
    af = AllFull((512, 512), save=True)
    df = append_all(df, af, cols, 'full')

    # add row for samples as percentage of total
    af_df = distribution_pct(df, cols)

    # drop first row
    af_df = af_df.iloc[1:]
    return af_df


def rs_full_df(cols: List) -> pd.DataFrame:
    """
        Create rough smooth class distribution table. Add percent samples
        column.
    """
    df = pd.DataFrame(columns=cols)

    # add rough smooth full dataset
    rsf = RoughSmoothFull((512, 512), save=True)
    df = append_rs(df, rsf, cols, 'full')

    # output rs full df
    rsf_df = df.loc[0, :].to_frame()

    # drop first row
    rsf_df = rsf_df.iloc[1:]
    rsf_df = rsf_df.transpose()

    # add row for samples as percentage of total
    rsf_df = distribution_pct(rsf_df, cols)
    return rsf_df


def rs_sub_df(cols: list) -> pd.DataFrame:
    """
        Create rough smooth subimage dataset class distribution table.
    """
    df = pd.DataFrame(columns=cols)

    # add subimage datasets, show samples for different sizes
    sizes = [(8, 8), (16, 16), (24, 24), (32, 32)]
    for size in sizes:
        temp = RoughSmoothSub(size, save=True)
        df = append_rs(df, temp, cols, 'sub')

    # output rs sub df
    # map first row to column headers
    df = df.transpose()
    df.columns = df.iloc[0]

    # drop first row
    df = df.iloc[1:]
    df.rename_axis('Label', axis=1, inplace=True)

    return df


if __name__ == '__main__':
    # columns for both dataset types
    all_cols = [_TYPE] + all_labels + [_TOTAL]
    rs_cols = [_TYPE] + rs_labels + [_TOTAL]

    # create tables
    af_df = all_full_df(all_cols)
    rsf_df = rs_full_df(rs_cols)
    rss_df = rs_sub_df(rs_cols)

    # log tables
    logger.info(af_df)
    logger.info(rsf_df)
    logger.info(rss_df)

    # save tables
    af_df.to_latex('./paper/tables/all_samples_full.tex')
    rsf_df.to_latex('./paper/tables/rs_samples_full.tex')
    rss_df.to_latex('./paper/tables/rs_samples_sub.tex')
