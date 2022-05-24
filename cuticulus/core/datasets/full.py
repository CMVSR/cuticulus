"""Full size image dataset with images resized to a specified input."""

import logging
import re
from glob import glob

import numpy as np
from beartype import beartype
from PIL import Image

from cuticulus.core.datasets.imutils import autocrop
from cuticulus.core.datasets.splitter import DatasetSplitter
from cuticulus.messages import not_considered

log = logging.getLogger('rich')


class FullDataset(DatasetSplitter):
    """Full size image dataset."""

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
        name = '{0}_full'.format(name)
        super().__init__(
            size=size,
            name=name,
            rebuild=rebuild,
            save=save,
        )

    @beartype
    def preprocess(self, img: np.ndarray) -> np.ndarray:
        """Preprocess the image.

        Automatically crop the images to squares centered on the middle of the
        image, where the ant head is typically located. Since this process is
        automatic, some images may not be cropped correctly.

        Args:
            img (np.ndarray): The image to preprocess.

        Returns:
            np.ndarray: The preprocessed image.
        """
        arr = autocrop(img)
        img = Image.fromarray(arr)
        img = img.resize(self.size, Image.ANTIALIAS)

        return super().preprocess(np.array(img))

    @beartype
    def build_dataset(self) -> tuple:
        """Process images.

         Returns:
            tuple: The ids and images.

        Raises:
            ValueError: Failed to create dataset.
        """
        images = []
        labels = []
        ids = []
        for fin in glob(str(self.base_path / 'data' / '*.jpg')):
            filename = re.search(r'[\d]+\.jpg', fin).group()
            iid = int(filename.split('.')[0])

            try:
                label = self.get_label(iid)
            except Exception:
                log.info(not_considered(iid))

            # get image and apply preprocessing
            img = self.preprocess(self.get_image(iid))
            images.append(img)
            labels.append(label)
            ids.append(iid)

        if len(images) != len(labels) != len(ids):
            raise ValueError('Number of images and labels do not match.')

        return (
            np.array(images),
            np.array(labels),
            np.array(ids),
        )
