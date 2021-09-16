
import logging
from typing import Type

import pandas as pd

# for debugging, env logging level must be set to debug/info
from cuticle_analysis.core import init
init()

from cuticle_analysis.datasets import Dataset  # noqa
from cuticle_analysis.models import Model  # noqa

logger = logging.getLogger(__name__)

RES_COLS = ['size', 'samples_per_class', 'run', 'test_loss', 'test_accuracy']


class ExperimentRunner:
    def __init__(self, name: str, dataset_type: Type[Dataset], model_type: Type[Model]):
        self.name = name
        self.dataset_type = dataset_type
        self.model_type = model_type

    def run(self,
            samples: int,
            size: tuple,
            runs: int = 10,
            epochs: int = 10,
            excludes: list = []):
        dataset = self.dataset_type(size=size, excludes=excludes, save=True)
        res_df = pd.DataFrame(columns=RES_COLS)

        for run in range(runs):
            model = self.model_type(dataset)
            model.train(epochs, samples)
            loss, acc = model.evaluate()

            # save results
            run_df = pd.DataFrame(
                [[size, samples, run, loss, acc]], columns=RES_COLS)
            res_df = res_df.append(run_df, ignore_index=True)
            res_df.to_csv(f'./output/{self.name}')
