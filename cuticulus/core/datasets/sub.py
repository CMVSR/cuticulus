"""Dataset of extracted subimage textures."""

import json
import logging
import re
from glob import glob

import numpy as np
from beartype import beartype
from PIL import Image

from cuticulus import const
from cuticulus.core.datasets.imutils import autocrop, shapes_to_label
from cuticulus.core.datasets.splitter import DatasetSplitter
from cuticulus.messages import not_considered

log = logging.getLogger('rich')


@beartype
def get_label_names(
    img: np.ndarray,
    seg_data: dict
) -> tuple:
    """Get all the segmented labels and their names.

    Creates an array where each pixel of the input image is assigned to a
    label.

    Args:
        img (np.ndarray): The image to process.
        seg_data (dict): The segmentation data.

    Returns:
        tuple: Tuple with (labeled_image, label_names).
    """
    # load segmented image data from json data
    label_map = {'_background_': 0}
    for shape in sorted(seg_data['shapes'], key=lambda x: x['label']):
        label_name = shape['label']
        if label_name in label_map:
            label_value = label_map.get(label_name)
        else:
            label_value = len(label_map)
            label_map[label_name] = label_value
    imglbl, _ = shapes_to_label(
        img.shape,
        seg_data['shapes'],
        label_map,
    )

    label_names = [None for _ in range(max(label_map.values()) + 1)]
    for name, value in label_map.items():
        label_names[value] = name

    return imglbl, label_names


class SubDataset(DatasetSplitter):
    """Subimage dataset."""

    @beartype
    def __init__(
        self,
        size: tuple[int, int],
        source_size: tuple[int, int],
        ds_type: str,
        name: str = '',
        rebuild: bool = False,
        save: bool = True,
    ):
        """Initialize the dataset.

        Args:
            size (tuple): Size of output subimages. Tuple with (rows, cols).
            source_size (tuple): Size of the source image to use.
            ds_type (str): The type of the dataset. (bg or rs)
            name (str): The name of the dataset.
            rebuild (bool): Whether to rebuild the dataset.
            save(bool): Whether to save the generated files for the dataset.
        """
        name = '{0}_sub'.format(name)
        self.source_size = source_size
        self.ds_type = ds_type
        super().__init__(
            size=size,
            name=name,
            rebuild=rebuild,
            save=save,
        )

    @beartype
    def preprocess(
        self,
        img: np.ndarray,
    ) -> np.ndarray:
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

        if self.source_size != const.NO_RESIZE:
            img = img.resize(self.source_size, Image.ANTIALIAS)

        return super().preprocess(np.array(img))

    @beartype
    def remap_points(
        self,
        rows: int,
        cols: int,
        points: list,
    ) -> list:
        """Remap the points to the new coordinates.

        Since the image is resized, the points need to be remapped to the new

        Args:
            rows (int): Number of rows in the raw image.
            cols (int): Number of columns in the raw image.
            points (list): List of points to remap.

        Returns:
            list: The remapped points.
        """
        length = min(rows, cols) // 2 - 1

        for point in points:
            # clip points outside of the new squared image
            if point[0] > length:
                point[0] = length
            if point[1] > length:
                point[1] = length

            if self.source_size != const.NO_RESIZE:
                # scale the points to the new scale
                point[0] = point[0] * self.source_size[0] / length
                point[1] = point[1] * self.source_size[1] / length

        return points

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

        rs_files = glob(str(self.base_path / 'rs' / '*.json'))
        bg_files = glob(str(self.base_path / 'bg' / '*.json'))
        files = rs_files + bg_files

        for pfile in files:
            # load image data based on avaiable jsons
            filename = re.search(r'[\d]+\.json', pfile).group()
            iid = int(filename.split('.')[0])

            if iid in ids:
                continue

            with open(pfile, 'r') as fin:
                seg_data = json.load(fin)

            try:
                label = self.get_label(iid)
            except Exception:
                log.info(not_considered(iid))

            img = self.preprocess(self.get_image(iid))
            for shape in seg_data['shapes']:
                seg_data['shapes'][0]['points'] = self.remap_points(
                    seg_data['imageHeight'],
                    seg_data['imageWidth'],
                    shape['points'],
                )
            lbl, label_names = get_label_names(img, seg_data)

            # pull 'cuticle data' from img as subimages
            rows, cols = self.size
            for row in range(0, lbl.shape[0] - rows, rows):
                for col in range(0, lbl.shape[1] - cols, cols):
                    x0, y0 = row, col
                    x1, y1 = (row + rows, col + cols)

                    pixellabels = lbl[x0:x1, y0:y1]
                    uniques = np.unique(pixellabels)
                    if len(uniques) > 1:
                        continue

                    sub_label = uniques[0]
                    sub_image = img[x0:x1, y0:y1]

                    # rough-smooth dataset only considers cuticle segments
                    if self.ds_type == 'rs':
                        if label_names[sub_label] == 'cuticle':
                            images.append(sub_image)
                            labels.append(label)
                            ids.append(iid)

                    # background dataset
                    else:
                        if label_names[sub_label] == 'cuticle':
                            # not background
                            labels.append(1)
                        else:
                            # background
                            labels.append(0)
                        images.append(sub_image)
                        ids.append(iid)

        if len(images) != len(labels) != len(ids):
            raise ValueError('Number of images and labels do not match.')

        return (
            np.array(images),
            np.array(labels),
            np.array(ids),
        )
