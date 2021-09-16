
import logging

from tensorflow.keras.models import Sequential
from tensorflow.keras import layers

from ..datasets import Dataset
from .model import TFModel

logger = logging.getLogger(__name__)


class CNN(TFModel):
    def __init__(self, data: Dataset):
        super().__init__('CNN', data)

        self.model = Sequential([
            layers.experimental.preprocessing.Rescaling(
                1./255,
                input_shape=(
                    self.size[0], self.size[1], 3)),
            layers.Conv2D(16, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(32, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(self.num_classes)
        ])
