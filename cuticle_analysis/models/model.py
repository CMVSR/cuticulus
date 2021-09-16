
from typing import List

from tensorflow import keras
import numpy as np

from ..datasets import Dataset


class Model:
    def __init__(self, name: str, data: Dataset):
        self.name = name
        self.data = data
        self.size = data.size
        self.num_classes = len(np.unique(data.labels))
        self.path = f'./output/model_{name}_{data.size[0]}_{data.size[1]}'

    def metadata(self) -> List[str]:
        return [
            f'Model Type: {self.name}'
        ]

    def save_weights(self) -> None:
        raise NotImplementedError

    def load_weights(self) -> None:
        raise NotImplementedError

    def train(self, epochs: int, samples_per_class: int) -> None:
        raise NotImplementedError


class TFModel(Model):
    def save_weights(self) -> None:
        self.model.save(self.path)

    def load_weights(self) -> None:
        self.model = keras.models.load_model(self.path)

    def train(self, epochs: int, samples_per_class: int) -> None:
        train_x, train_y = self.data.stratified_split(samples_per_class)
        val_x, val_y = self.data.build_validation_set()

        # compile
        self.model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=[
                'accuracy',
                'mean_squared_error',
                'categorical_crossentropy',
                'precision',
                'recall',
            ]
        )
        self.model.summary()

        # fit
        self.epochs = epochs
        self.history = self.model.fit(
            train_x,
            train_y,
            epochs=epochs,
            validation_data=(val_x, val_y),
            verbose=1
        )

    def predict(self, image: np.ndarray) -> np.ndarray:
        pred = self.model.predict(image)
        pred = np.argmax(pred, axis=1)
        return pred

    def evaluate(self):
        test_x, test_y = self.data.test_set()
        return self.model.evaluate(test_x, test_y, batch_size=128)
