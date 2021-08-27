
from typing import Dict
import gc
import logging

import pandas as pd

# for debugging, env logging level must be set to debug/info
from cuticle_analysis.core import init
init()

from cuticle_analysis.datasets import AllFull  # noqa
from cuticle_analysis.datasets import RoughSmoothFull  # noqa
from cuticle_analysis.datasets import RoughSmoothSub  # noqa

logger = logging.getLogger(__name__)


all_cols = [
    'type',
    'rough dimpled',
    'rough netted',
    'rough ridged',
    'rough T',
    'smooth gritty',
    'smooth smooth',
    'total'
]
rs_cols = [
    'type',
    'rough',
    'smooth',
    'total'
]


def total_samples(class_data: Dict) -> int:
    """
    Total number of samples in the dataset.
    """
    res = 0
    for _, data in class_data.items():
        res += data
    return res


def all_row(type: str, class_data: Dict) -> pd.DataFrame:
    row = pd.DataFrame([[
        type,
        class_data['rough dimpled'],
        class_data['rough netted'],
        class_data['rough ridged'],
        class_data['rough T'],
        class_data['smooth gritty'],
        class_data['smooth smooth'],
        total_samples(class_data)
    ]], columns=all_cols)
    return row


def rs_row(type: str, size: tuple, class_data: Dict) -> pd.DataFrame:
    if type != 'full':
        type = f'{type}_{size}'

    row = pd.DataFrame([[
        type,
        class_data['rough'],
        class_data['smooth'],
        total_samples(class_data)
    ]], columns=rs_cols)
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
logger.info("number of samples per class per dataset")
logger.info(all_df.transpose())
logger.info(rs_df.transpose())

# save to file
all_df.transpose().to_latex('./paper/tables/all_samples_int.tex')
rs_df.transpose().to_latex('./paper/tables/rs_samples_int.tex')

logger.info("\n samples per class as percentage")
all_df.loc[:, all_cols[1:]] = all_df.loc[:, all_cols[1:]].div(
    all_df["total"], axis=0) * 100
rs_df.loc[:, rs_cols[1:]] = rs_df.loc[:, rs_cols[1:]].div(
    rs_df["total"], axis=0) * 100
all_df = all_df.drop(columns=['total'])
rs_df = rs_df.drop(columns=['total'])
logger.info(all_df)
logger.info(rs_df)

# save to file
all_df.to_latex('./paper/tables/all_samples_pct.tex')
rs_df.to_latex('./paper/tables/rs_samples_pct.tex')
