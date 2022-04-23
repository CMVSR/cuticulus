"""Full size dataset, considering all classes."""

from beartype import beartype

from cuticulus.core.datasets.full import FullDataset


class AllFull(FullDataset):
    """Full size dataset, considering all classes."""

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
        name = '{0}_all'.format(name)
        super().__init__(size, name, rebuild, save)
