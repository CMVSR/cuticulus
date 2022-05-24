"""Dataset to discern background."""

from beartype import beartype

from cuticulus import const
from cuticulus.core.datasets.sub import SubDataset


class BackgroundSub(SubDataset):
    """Subimage dataset, considering only background."""

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
        name = '{0}_bg_{1}_{2}'.format(name, *source_size)
        super().__init__(
            size=size,
            source_size=source_size,
            ds_type='bg',
            name=name,
            rebuild=rebuild,
            save=save,
        )
