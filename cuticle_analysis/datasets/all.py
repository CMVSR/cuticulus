
from typing import Dict

from .. import const
from .full import FullDataset


class AllFull(FullDataset):
    'Full sized image dataset with all original labels.'

    def __init__(self,
                 size: tuple,
                 excludes: list = None,
                 random_seed: int = None,
                 rebuild: bool = False,
                 save: bool = False):
        name = f'all'
        d_type = const.DATASET_ALL  # used for converting labels
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
            res[const.INT_ALL_LABEL_MAP[k]] = v
        return res


class AllFullAugmented(FullDataset):
    'Full sized image dataset with all original labels and augmented data.'

    def __init__(self,
                 size: tuple,
                 excludes: list = None,
                 random_seed: int = None,
                 rebuild: bool = False,
                 save: bool = False):
        name = f'all_augmented'
        d_type = const.DATASET_ALL  # used for converting labels
        super().__init__(size,
                         name=name,
                         d_type=d_type,
                         excludes=excludes,
                         random_seed=random_seed,
                         rebuild=rebuild,
                         save=save)
        self.augment()

    def augment(self):
        # self.images, self.labels = self.images, self.labels
        raise NotImplementedError
