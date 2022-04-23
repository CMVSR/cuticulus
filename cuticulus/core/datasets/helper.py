"""Helper for dataset access."""

import numpy as np
import pandas as pd
from beartype import beartype
from PIL import Image

from cuticulus.core.datasets.downloader import Downloader


@beartype
def get_str_df(row: pd.DataFrame, col: str) -> str:
    """Get string from pandas series row and column.

    Args:
        row (pd.DataFrame): Row of dataframe.
        col (str): Column name.

    Returns:
        str: String with binomial info.
    """
    return str(row[col].values[0]).lower()


class DatasetHelper(Downloader):
    """A helper class for functions relating to basic dataset access."""

    @beartype
    def __init__(
        self,
        name: str,
        size: tuple[int, int] = (0, 0),
    ):
        """Initialize the helper class.

        If rows and cols are not specified by the size tuple parameter, the
        images will retain their original size. Otherwise, they will be
        reshaped to match (rows, cols). See DatasetHelper for more info.

        Args:
            name (str): The name of the dataset. Defaults to 'base'.
            size (tuple): Tuple with (rows, cols).
        """
        super().__init__()
        self.name = name

        rows, cols = size
        self.size = size
        self.rows = rows
        self.cols = cols

        self.raw_meta_path = self.base_path / 'labels.xlsx'
        self.raw_meta = pd.read_excel(self.raw_meta_path, header=0)

    @beartype
    def get_image(self, iid: int) -> np.ndarray:
        """Get the image data for a given image ID.

        Args:
            iid (int): The ID of the ant image to get.

        Returns:
            np.ndarray: The image data.
        """
        path = str(self.base_path / 'data' / '{0}.jpg'.format(iid))
        return np.array(Image.open(path))

    @beartype
    def get_binomial(self, iid: int) -> dict:
        """Get the binomial data for an ant given image ID.

        Args:
            iid (int): The ID of the ant image to get.

        Returns:
            dict: The binomial data.
        """
        row = self.raw_meta.loc[self.raw_meta['Photo_number'] == iid]
        binoms = ['Sub-species', 'Species', 'Genus', 'Sub-Family']
        return {
            binom: get_str_df(row, binom)
            for binom in binoms
            if not row[binom].isnull().any()
        }
