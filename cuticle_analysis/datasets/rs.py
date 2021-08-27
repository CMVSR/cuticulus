
from typing import Dict

from .. import const
from .full import FullDataset
from .sub import SubDataset


class RoughSmoothFull(FullDataset):
    'Full sized image dataset with rough and smooth labels only.'

    def __init__(self,
                 size: tuple,
                 excludes: list = None,
                 random_seed: int = None,
                 rebuild: bool = False,
                 save: bool = False):
        name = f'rs'
        d_type = const.DATASET_RS  # used for converting labels to rough or smooth
        super().__init__(size,
                         name=name,
                         d_type=d_type,
                         excludes=excludes,
                         random_seed=random_seed,
                         rebuild=rebuild,
                         save=save)

    def class_data(self) -> Dict:
        """Return class data for the dataset.

        Returns:
            Dict: Class data for the dataset.
        """
        temp = super().class_data()
        res = {}
        for k, v in temp.items():
            res[const.INT_RS_LABEL_MAP[k]] = v
        return temp


class RoughSmoothSub(SubDataset):
    'Subimage dataset with rough and smooth labels only.'

    def __init__(self,
                 size: tuple,
                 excludes: list = None,
                 random_seed: int = None,
                 rebuild: bool = False,
                 save: bool = False):
        name = f'rs'
        d_type = const.DATASET_RS  # used for converting labels to rough or smooth
        super().__init__(size,
                         name=name,
                         d_type=d_type,
                         excludes=excludes,
                         random_seed=random_seed,
                         rebuild=rebuild,
                         save=save)

    def class_data(self) -> Dict:
        """Return class data for the dataset.

        Returns:
            Dict: Class data for the dataset.
        """
        temp = super().class_data()
        res = {}
        for k, v in temp.items():
            res[const.INT_RS_LABEL_MAP[k+1]] = v
        return res
