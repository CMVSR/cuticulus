"""Class for predicting the class of existing ant images."""

import os
from glob import glob
from pathlib import Path

import numpy as np
from beartype import beartype
from PIL import Image

from cuticulus.console import console
from cuticulus.core.models.helper import ModelHelper


class Predictor(object):
    """Class for predicting the class of existing ant images."""

    @beartype
    def __init__(self, model: ModelHelper):
        """Initialize the Predictor class.

        Args:
            model (ModelHelper): The model to use for prediction.
        """
        self.model = model
        self.base_path = Path.cwd() / 'input'

        if not self.base_path.exists():
            os.mkdir(self.base_path)

    def run(self):
        """Run the prediction on each file and print the output."""
        console.log('Predicting files in "{0}"'.format(self.base_path))
        for fin in glob(str(self.base_path / '*.jpg')):
            console.log('Predicting "{0}"'.format(fin))
            image = np.array(Image.open(fin))
            pred = self.predict(image)
            console.log('Predicted class: {0}'.format(pred))

    def predict(self, image: np.ndarray) -> np.ndarray:
        """Predict the class of the input image.

        Args:
            image (np.ndarray): The image to predict the class of.

        Returns:
            np.ndarray: The predicted class.
        """
        image = self.model.ds.preprocess(image)
        image = self.model.preprocess(image)
        return self.model.predict(image)
