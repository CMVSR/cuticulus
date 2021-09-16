
import logging
from typing import Tuple

from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow import keras
import numpy as np

from ..datasets import Dataset
from .model import Model

logger = logging.getLogger(__name__)


class CNN(Model):
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

    def train(self, epochs: int, samples_per_class: int) -> None:
        train_x, train_y = self.data.stratified_split(samples_per_class)
        val_x, val_y = self.data.build_validation_set()

        self.model.compile(
            optimizer='adam',
            loss=keras.losses.SparseCategoricalCrossentropy(
                from_logits=True),
            metrics=['accuracy'])
        self.model.summary()
        self.epochs = epochs

        self.history = self.model.fit(
            train_x, train_y,
            validation_data=(val_x, val_y),
            epochs=epochs
        )

    def predict(self, image: np.ndarray) -> np.ndarray:
        pred = self.model.predict(image)
        pred = np.argmax(pred, axis=1)
        return pred

    def evaluate(self) -> Tuple[float, float]:
        test_x, test_y = self.data.test_set()
        loss, acc = self.model.evaluate(test_x, test_y, batch_size=128)
        return loss, acc
