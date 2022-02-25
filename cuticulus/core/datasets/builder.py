"""Module for building generated files from base dataset."""

import logging

import numpy as np
from beartype import beartype

from cuticulus import const
from cuticulus.console import console
from cuticulus.core.datasets.labels import convert_labels
from cuticulus.core.datasets.loader import DatasetLoader

log = logging.getLogger('rich')


class DatasetBuilder(DatasetLoader):
    """A class for building the dataset."""

    @beartype
    def __init__(
        self,
        size: tuple[int, int] = (0, 0),
        name: str = '',
        rebuild: bool = False,
        save: bool = True,
    ):
        """Initialize the dataset.

        If rows and cols are not specified by the size tuple parameter, the
        images will retain their original size. Otherwise, they will be
        reshaped to match (rows, cols). See DatasetHelper for more info.

        Args:
            size (tuple): Tuple with (rows, cols).
            name (str): The name of the dataset.
            rebuild (bool): Whether to rebuild the dataset.
            save(bool): Whether to save the generated files for the dataset.
        """
        super().__init__(name, size=size)
        self.rebuild = rebuild
        self.save = save

        # load the metadata and dataset
        self.load()
        self.print_data()

    @beartype
    def get_label(self, iid: int) -> int:
        """Get the label for the given image id.

        Args:
            iid (int): The image id.

        Returns:
            int: The label.
        """
        idx = np.where(self.meta[0] == iid)
        label = self.meta[1][idx]

        try:
            return int(label)
        except Exception:
            return int(label[0])

    @beartype
    def preprocess(self, img: np.ndarray) -> np.ndarray:
        """Preprocess an image.

        Args:
            img (np.ndarray): The image.

        Returns:
            np.ndarray: The preprocessed image.
        """
        return img

    def load_labels(self):
        """Load metadata file for labels."""
        # load metadata
        if self.rebuild or not self.meta_path.exists():
            console.log('Building labels.')
            self.meta = self.build_labels()
            console.log('Built labels.')

            if self.save:
                np.save(self.meta_path, self.meta)
        else:
            self.meta = np.load(self.meta_path)
            console.log('Loaded labels.')

    def load_images(self):
        """Load images, labels, and ids files."""
        images_exists = self.images_path.exists()
        images_exists = images_exists and self.labels_path.exists
        images_exists = self.ids_path.exists()

        # load images, labels, ids
        if self.rebuild or not images_exists:
            console.log('Building dataset.')
            images, labels, ids = self.build_dataset()
            self.images = images
            self.labels = labels
            self.ids = ids
            console.log('Built dataset.')

            if self.save:
                np.save(self.images_path, self.images)
                np.save(self.labels_path, self.labels)
                np.save(self.ids_path, self.ids)
        else:
            self.images = np.load(self.images_path, allow_pickle=True)
            self.labels = np.load(self.labels_path, allow_pickle=True)
            self.ids = np.load(self.ids_path, allow_pickle=True)
            console.log('Loaded dataset.')

    def load(self):
        """Load all generated files from raw dataset."""
        self.load_labels()
        self.load_images()

    @beartype
    def print_labels(self, labels: np.ndarray):
        """Print the numbre of samples for each class label.

        Args:
            labels (np.ndarray): The labels.
        """
        console.log('Samples per class:')
        uniques, counts = np.unique(labels, return_counts=True)
        for idx, _ in enumerate(uniques):
            console.log('{0}: {1}'.format(uniques[idx], counts[idx]))

    def print_data(self):
        """Print information about the dataset."""
        console.log('Unique images considered: {0}'.format(len(self.ids)))
        self.print_labels(self.labels)

    def build_labels(self):
        """Process labels spreadsheet.

        Returns:
            np.array: The labels.
        """
        df = convert_labels(
            self.raw_meta[list(const.LABEL_COLS)].mode(axis=1)[0],
        )

        # clip by max values
        maxv = int(df['class'].max())
        idx = df['class'].isin(range(0, maxv + 1))
        df = df.loc[idx]

        # setup id column
        id_col = self.raw_meta['Photo_number']
        id_col = id_col.to_frame('id')
        id_col = id_col.loc[idx.values]

        # store as arrays
        img_labels = df['class'].values.astype(int)
        img_ids = id_col['id'].values.astype(int)

        return np.stack([img_ids, img_labels])
