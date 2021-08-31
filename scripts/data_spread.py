
from typing import Dict
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

# output
# add row for samples as percentage of total
samples_pct = all_df.loc[:, all_cols[1:]].div(
    all_df[_TOTAL], axis=0)
samples_pct = samples_pct.astype(float).round(2)
all_df = all_df.append(samples_pct, ignore_index=True)
all_df = all_df.transpose().rename(
    columns={_TYPE: 'Label', 0: 'Samples (n)', 1: 'Samples (%)'})
rs_df = rs_df.transpose()

# drop first row
all_df = all_df.iloc[1:]

# save to file
logger.info(all_df)
logger.info(rs_df)
all_df.to_latex('./paper/tables/all_samples_int.tex')
rs_df.to_latex('./paper/tables/rs_samples_int.tex')

# rs_df.loc[:, rs_cols[1:]] = rs_df.loc[:, rs_cols[1:]].div(
#     rs_df[_TOTAL], axis=0) * 100
