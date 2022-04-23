"""Module for setting up dataset paths for DatasetBuilder."""

from beartype import beartype

from cuticulus.core.datasets.helper import DatasetHelper


class DatasetLoader(DatasetHelper):
    """A class for loading the dataset."""

    @beartype
    def __init__(
        self,
        name: str,
        size: tuple[int, int] = (0, 0),
    ):
        """Initialize the dataset.

        Args:
            name (str): The name of the dataset. Defaults to ''.
            size (tuple): Tuple with (rows, cols).
        """
        super().__init__(name, size=size)

        # paths
        if getattr(self, 'size', None):
            default = '{0}_{1}_{2}'.format(self.name, self.rows, self.cols)
        else:
            default = '{0}_full'.format(self.name)

        self.dir_path = self.base_path / default
        if not self.dir_path.exists():
            self.dir_path.mkdir(parents=True)

        self.meta_path = self.base_path / default / 'meta.npy'
        self.images_path = self.base_path / default / 'images.npy'
        self.labels_path = self.base_path / default / 'labels.npy'
        self.ids_path = self.base_path / default / 'ids.npy'
