
from typing import List, Tuple

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
        self.model.save(self.path)

    def load_weights(self) -> None:
        self.model = keras.models.load_model(self.path)

    def train(self, epochs: int, samples_per_class: int) -> None:
        raise NotImplementedError()

    def predict(self, image: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    def evaluate(self) -> Tuple[float, float]:
        raise NotImplementedError()
