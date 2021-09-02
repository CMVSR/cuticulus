
import logging
from typing import Dict

import cv2
import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


class DatasetHelper():
    """
        A helper class for the Dataset class for functions relating to basic
        dataset access.
    """

    def __init__(self):
        self.ant_data = pd.read_excel(f'./dataset/labels.xlsx', header=0)

    def get_image(self, _id: int) -> np.ndarray:
        """Get image by ID.

        Args:
            _id (int): ID of the sample.

        Returns:
            img (np.ndarray): Image as cv2 image object (numpy array).
        """
        path = f'./dataset/data/{_id}.jpg'
        img = cv2.imread(path)

        if img is None:
            msg = f'Failed to open image {path}'
            logger.error(msg)
            raise ValueError(msg)

        return img

    def get_ant_info(self, _id: int) -> Dict:
        """Get ant species info from original dataset.

        Args:
            _id (int): ID of the sample.

        Returns:
            Dict[str]: List of ant species info.
        """
        row = self.ant_data.loc[self.ant_data['Photo_number'] == _id]

        res = {}
        if not row['Sub-species'].isnull().any():
            res['subspecies'] = str(row["Sub-species"].values[0]).lower()
        if not row['Species'].isnull().any():
            res['species'] = str(row["Species"].values[0]).lower()
        if not row['Subgenus'].isnull().any():
            res['subgenus'] = str(row["Subgenus"].values[0]).lower()
        if not row['Genus'].isnull().any():
            res['genus'] = str(row["Genus"].values[0]).lower()
        if not row['Sub-Family'].isnull().any():
            res['subfamily'] = str(row["Sub-Family"].values[0]).lower()

        return res
