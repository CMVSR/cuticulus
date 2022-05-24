"""Dataset only considering only rough and smooth."""

import numpy as np
from beartype import beartype

from cuticulus import const
from cuticulus.core.datasets.full import FullDataset
from cuticulus.core.datasets.sub import SubDataset


@beartype
def build_labels(labels) -> np.ndarray:
    """Process labels spreadsheet. Convert labels to rough and smooth.

    Returns:
        np.array: The ids and labels.
    """
    # res[1] holds labels, 0-3 represent rough
    idx = np.where(labels[1, :] < 4)
    labels[1, :][idx] = 0

    # 4 represents smooth
    idx = np.where(labels[1, :] == 4)
    labels[1, :][idx] = 1

    return labels


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
        return build_labels(super().build_labels())


class RoughSmoothSub(SubDataset):
    """Subimage dataset, considering only rough and smooth."""

    @beartype
    def __init__(
        self,
        size: tuple[int, int],
        source_size: tuple[int, int] = const.NO_RESIZE,
        name: str = '',
        rebuild: bool = False,
        save: bool = True,
    ):
        """Initialize the dataset.

        Args:
            size (tuple): Size of output subimages. Tuple with (rows, cols).
            source_size (tuple): Size of the source image to use.
            name (str): The name of the dataset.
            rebuild (bool): Whether to rebuild the dataset.
            save(bool): Whether to save the generated files for the dataset.
        """
        name = '{0}_rs_{1}_{2}'.format(name, *source_size)
        super().__init__(
            size=size,
            source_size=source_size,
            ds_type='rs',
            name=name,
            rebuild=rebuild,
            save=save,
        )

    @beartype
    def build_labels(self) -> np.ndarray:
        """Process labels spreadsheet. Convert labels to rough and smooth.

        Returns:
            np.array: The ids and labels.
        """
        return build_labels(super().build_labels())
