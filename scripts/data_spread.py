
from typing import Dict, List
import gc
import logging

import pandas as pd

# for debugging, env logging level must be set to debug/info
from cuticle_analysis.core import init
init()

from cuticle_analysis import const  # noqa
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

all_cols = [_TYPE] + all_labels + [_TOTAL]
rs_cols = [_TYPE] + rs_labels + [_TOTAL]


def total_samples(class_data: Dict) -> int:
    """
    Total number of samples in the dataset.
    """
    res = 0
    for _, data in class_data.items():
        res += data
    return res


def all_row(type: str, class_data: Dict) -> pd.DataFrame:
    data = [class_data[label] for label in all_labels]
    cols = [type] + data + [total_samples(class_data)]
    row = pd.DataFrame(
        [cols], columns=all_cols)
    return row


def rs_row(type: str, size: tuple, class_data: Dict) -> pd.DataFrame:
    if type != 'full':
        type = f'{type}_{size}'

    data = [class_data[label] for label in rs_labels]
    cols = [type] + data + [total_samples(class_data)]
    row = pd.DataFrame([cols], columns=rs_cols)
    return row


# init output tables
all_df = pd.DataFrame(columns=all_cols)
rs_df = pd.DataFrame(columns=rs_cols)

# add all full dataset
af = AllFull((512, 512), save=True)
all_df = all_df.append(all_row('full', af.class_data()), ignore_index=True)
del af
gc.collect()

# add rough smooth full dataset
rsf = RoughSmoothFull((512, 512), save=True)
rs_df = rs_df.append(
    rs_row('full', rsf.size, rsf.class_data()), ignore_index=True)
del rsf
gc.collect()

# add subimage datasets, show samples for different sizes
sizes = [(8, 8), (16, 16), (32, 32), (64, 64)]
for size in sizes:
    temp = RoughSmoothSub(size, save=True)
    rs_df = rs_df.append(
        rs_row('sub', size, temp.class_data()), ignore_index=True)
    del temp
    gc.collect()


def distribution_pct(df: pd.DataFrame, cols: List) -> pd.DataFrame:
    """
    Calculate the distribution of a class in a dataframe as a percent.
    Returns:
        df: Transposed dataframe with the columns ['Label', 'Samples (n)', 'Samples (%)']
    """
    sample_pct = df.loc[:, cols[1:]].div(
        df[_TOTAL], axis=0).astype(float).round(2)
    df = df.append(sample_pct, ignore_index=True)
    return df.transpose().rename(
        columns={_TYPE: 'Label', 0: 'Samples (n)', 1: 'Samples (%)'})


def save_all_full_df(df: pd.DataFrame, cols: List) -> None:
    """
    Save the dataframe to a latex file. Add percent samples column.
    """
    # add row for samples as percentage of total
    all_full_df = distribution_pct(df, cols)

    # drop first row
    all_full_df = all_full_df.iloc[1:]

    # save to file
    logger.info(all_full_df)
    all_full_df.to_latex('./paper/tables/all_samples_full.tex')


def save_rs_df(df: pd.DataFrame, cols: List) -> None:
    # output rs full df
    rs_full_df = df.loc[0, :].to_frame()

    # drop first row
    rs_full_df = rs_full_df.iloc[1:]
    rs_full_df = rs_full_df.transpose()

    # add row for samples as percentage of total
    rs_full_df = distribution_pct(rs_full_df, cols)

    logger.info(rs_full_df)
    rs_full_df.to_latex('./paper/tables/rs_samples_full.tex')


if __name__ == '__main__':
    save_all_full_df(all_df, all_cols)
    save_rs_df(rs_df, rs_cols)
