"""Full size dataset, considering only rough and smooth."""

import numpy as np
from beartype import beartype

from cuticulus.core.datasets.full import FullDataset


class RoughSmoothFull(FullDataset):
    """Full size dataset, considering only rough and smooth."""

    @beartype
    def __init__(
        self,
        size: tuple[int, int],
        name: str = '',
        rebuild: bool = False,
        save: bool = True,
    ):
        """Initialize the dataset.

        Args:
            size (tuple): Tuple with (rows, cols).
            name (str): The name of the dataset.
            rebuild (bool): Whether to rebuild the dataset.
            save(bool): Whether to save the generated files for the dataset.
        """
        name = '{0}_rs'.format(name)
        super().__init__(size, name, rebuild, save)

    @beartype
    def build_labels(self) -> np.ndarray:
        """Process labels spreadsheet. Convert labels to rough and smooth.

        Returns:
            np.array: The ids and labels.
        """
        res = super().build_labels()

        # res[1] holds labels, 0-3 represent rough
        idx = np.where(res[1, :] < 4)
        res[1, :][idx] = 0

        # 4 represents smooth
        idx = np.where(res[1, :] == 4)
        res[1, :][idx] = 1

        return res
